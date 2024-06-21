import flet as ft
from openai import OpenAI
import os
import time

openai_key = os.environ.get('OPENAI_API_KEY')

client = OpenAI(api_key=openai_key)

with open('assistants.txt', 'r') as f:
    assistant_ids = [line.strip() for line in f]

assistants = [client.beta.assistants.retrieve(id) for id in assistant_ids]
threads = [client.beta.threads.create() for _ in range(len(assistants))]


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ALWAYS
    page.title = 'Prompt Testing'

    def handle_close(e):
        dlg.open = False
        page.update()

    dlg = ft.AlertDialog(
        title=ft.Text("Error"),
        content=ft.Text("Invalid assistant ID"),
        actions=[ft.TextButton("OK", on_click=handle_close)]
    )

    def add_assistant(e):
        assistant_id = new_assistant_id.value
        new_assistant_id.value = ''

        if not assistant_id:
            return

        print(f'adding assistant {assistant_id}')
        print('retrieving assistant')
        try:
            print('trying to retrieve assistant')
            assistant = client.beta.assistants.retrieve(assistant_id)
        except Exception as e:
            print('error retrieving assistant')
            print(e)
            page.overlay.append(dlg)
            dlg.open = True
            page.update()
            # print(e)
            return
        print('creating thread')
        thread = client.beta.threads.create()
        col = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, alignment=ft.MainAxisAlignment.CENTER)

        assistants.append(assistant)
        threads.append(thread)
        cols.append(col)

        page.controls[2].controls.insert(-1, ft.Text(f'{assistant.name} ({assistant.id})', selectable=True))
        # page.controls[2].controls.append(col)
        with open('assistants.txt', 'a') as f:
            f.write(assistant_id + '\n')
        print('added new assistant and thread')
        page.update()

    def generate_response(prompt):
        if not prompt or len(assistants) == 0:
            return
        print('generating new response')
        messages = []
        runs = []
        for i in range(len(assistants)):
            messages.append(client.beta.threads.messages.create(
                thread_id=threads[i].id,
                role='user',
                content=prompt
            ))

            cols[i].controls.append(
                ft.Row(controls=[
                    ft.CircleAvatar(content=ft.Text("User"), radius=12),
                    ft.Text("You: ", size=12)]
                )
            )
            cols[i].controls.append(ft.Text(prompt))
            page.update()

            runs.append(client.beta.threads.runs.create(
                thread_id=threads[i].id,
                assistant_id=assistants[i].id,
            ))

        for i in range(len(assistants)):
            while runs[i].status != 'completed':
                time.sleep(0.5)
                runs[i] = client.beta.threads.runs.retrieve(
                    thread_id=threads[i].id,
                    run_id=runs[i].id
                )
                print(f'run{i+1} status: {runs[i].status}')
            print(f'finished generating response {i+1}')

            messages[i] = client.beta.threads.messages.list(
                thread_id=threads[i].id
            )

            response = messages[i].data[0].content[0].text.value

            cols[i].controls.append(
                ft.Row(controls=[
                    ft.CircleAvatar(content=ft.Text("Bot"), radius=12),
                    ft.Text(f"{assistants[i].name}: ", size=12)]
                )
            )
            cols[i].controls.append(ft.Text(response, selectable=True))
            page.update()
        # end of generate_response function

    def on_button_click(e):
        if page.controls[0].visible and page.controls[1].visible:
            page.controls[0].visible = False
            page.controls[1].visible = False
            row.controls[-1].visible = False

        prompt = new_message.value
        new_message.value = ''

        if not prompt:
            return

        generate_response(prompt)
        # end of on_button_click function

    def layout(e):
        print('showing layout')
        print('page controls:', page.controls)
        print('rows:')
        for control in page.controls:
            try:
                print(control.controls)
            except AttributeError:
                print(control)
        print('cols:', cols)

    def remove_assistant(e, assistant_id):
        if len(assistants) == 0:
            return

        print(assistant_ids)
        # Find the index of the assistant with the given ID
        print(f"removing assistant {assistant_id}")
        i = assistants.index(client.beta.assistants.retrieve(assistant_id))
        print(f"found assistant at index {i} {assistant_ids[i]}")

        # Remove assistant, thread, and column from their lists
        del assistants[i]
        del threads[i]
        del cols[i]
        del row.controls[i]

        # Remove assistant's ID from the file
        with open('assistants.txt', 'r') as f:
            lines = f.readlines()
        with open('assistants.txt', 'w') as f:
            for line in lines:
                if line.strip() != assistant_id:
                    f.write(line)
        # Update the UI
        page.update()
        print('removed assistant')
    # variables
    cols = [ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS, alignment=ft.MainAxisAlignment.CENTER) for _ in range(len(assistants))]

    new_message = ft.TextField(label='Message', hint_text='Say something...')

    new_assistant_id = ft.TextField(label='Assistant ID')
    add_button = ft.ElevatedButton("Add Assistant", on_click=add_assistant, bgcolor=ft.colors.BLUE_GREY_800)
    show = ft.ElevatedButton("Show", on_click=layout, bgcolor=ft.colors.BLUE_GREY_800)

    button = ft.ElevatedButton("Send", on_click=on_button_click, bgcolor=ft.colors.BLUE_GREY_800)

    row = ft.Row(controls=[], alignment=ft.MainAxisAlignment.CENTER, scroll=ft.ScrollMode.ALWAYS)

    for i in range(len(assistants)):
        row.controls.append(ft.Column([ft.Text(f'{assistants[i].name} ({assistants[i].id})', selectable=True)]))

    row.controls.append(ft.ElevatedButton("Remove", on_click=lambda e: remove_assistant(e, assistants[len(assistants) - 1].id), bgcolor=ft.colors.RED_800))

    page.add(
        ft.Row(controls=[new_assistant_id, add_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        row,
        ft.Divider(),
        ft.Row(controls=cols, alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        ft.Row(controls=[new_message, button, show], alignment=ft.MainAxisAlignment.CENTER)
    )


ft.app(target=main, view=ft.AppView.FLET_APP)
