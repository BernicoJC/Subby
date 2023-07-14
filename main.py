from flet import *
from datetime import date

def main(page: Page):
    class SubGoal:
        title = ""
        note = ""
        time = 0
        point = 1
        date_achieved = ""

        def __init__(self, title, note, time, point):
            self.title = title
            self.note = note
            if not str(time).isnumeric():
                self.time = 0
            else:
                self.time = int(time)
            self.point = point
            self.date_achieved = ""

            self.done = False
        
        def assign_point(self, x):
            self.point = x
            update_long_main()
            update_weekly_main()

        def check(self, e):
            self.done = True
            self.date_achieved = str(date.today())
            current_goal[0].update_progress()
            current_goal[0].check_goal(None)
            update_long_main()
            update_weekly_main()

        def uncheck(self, e):
            self.done = False
            self.date_achieved = ""
            current_goal[0].update_progress()
            current_goal[0].check_goal(None)
            update_long_main()
            update_weekly_main()
        
        def main_display(self):
            x = Container(
                    bgcolor=colors.SURFACE_VARIANT if not self.done else colors.GREEN,

                    content = Column(
                        [
                            Text(self.title.title(), size=15, max_lines=1), 
                        ],
                        spacing = 0,
                    ),
                    
                    alignment=alignment.center_left,
                    margin=5,
                    padding= padding.only(left=12, right=12, top=6),
                    width=300,
                    height=35,
                    border_radius=5, # rounded rectangle
                    ink=True,

                    on_click = self.check_subgoal
                )
        
            return x

        slider = Slider(min=1, max=10, divisions=9, label="{value}", value=int(point))

        def edit_button(self, e):
            self.assign_point(self.slider.value)
            current_goal[0].check_goal(None)
            page.go("/check_goal")

        def check_subgoal(self, e):
            self.slider.value = int(self.point)
            check_subgoal_contents.clear()

            check_subgoal_contents_container = []
            check_subgoal_contents.append(AppBar(title=Text(self.title), bgcolor=colors.SURFACE_VARIANT))
            check_subgoal_contents_container.append(Text(value= "Time: " + str(self.time) + " days"))
            check_subgoal_contents_container.append(Text(value= "Note: " + self.note))
            check_subgoal_contents_container.append(Text(value= "Points: " + str(int(self.point))))

            check_subgoal_contents.append(
                Container(
                    bgcolor=colors.SURFACE_VARIANT,
                    
                    content = Column(check_subgoal_contents_container),

                    alignment=alignment.top_left,
                    margin=5,
                    padding= padding.only(left=12, right=12, top=6),
                    width=300,
                    height=100,
                    border_radius=5, # rounded rectangle
                    ink=True,
                )
            )
            if not self.done:
                check_subgoal_contents.append(Divider())
                check_subgoal_contents.append(Text(value="Edit Point"))
                check_subgoal_contents.append(self.slider)
                check_subgoal_contents.append(ElevatedButton(text="Submit", on_click=self.edit_button))
            
            if self.done:
                check_subgoal_contents.append(Text(value= "Date Achieved: " + self.date_achieved))

            check_subgoal_contents.append(
                Container(
                    bgcolor=colors.GREEN if not self.done else colors.RED,
                    content = Icon(icons.CHECK) if not self.done else Text(value="Cancel"),

                    alignment=alignment.center,
                    margin=5,
                    padding=20,
                    width=300,
                    height=65,
                    border_radius=5, # rounded rectangle
                    ink=True,

                    on_click=self.check if not self.done else self.uncheck
                )
            )
            page.go("/check_subgoal")

    class Goal:
        title = ""
        target = ""
        note = ""
        points_collected = 0
        date_achieved = ""
        subgoals = []

        def __init__(self, title, target, note, long_term):
            self.title = title
            self.date_added = str(date.today())
            self.target = target
            self.note = note
            self.long_term = long_term
            self.subgoals = []
            self.progress = 0
            self.total_point = 0
            self.points_collected = 0
            self.time = 0

        def reset_progress(self, e):
            for i in self.subgoals:
                i.uncheck(None)
            page.go("/check_goal")

        def reset_progress_all(self, e):
            for i in self.subgoals:
                i.uncheck(None)

        def update_time(self):
            self.time = 0
            for i in self.subgoals:
                if not i.done:
                    self.time = self.time + i.time

        def update_progress(self):
            self.progress = 0
            self.total_point = 0
            self.points_collected = 0

            for i in self.subgoals:
                self.total_point = self.total_point + i.point
            
            for i in self.subgoals:
                if i.done:
                    self.points_collected = self.points_collected + i.point
            self.progress = self.points_collected / self.total_point if self.total_point != 0 else 0
            update_long_main()
            update_weekly_main()

        def to_display(self, with_button):
            x = Container(
                    bgcolor=colors.SURFACE_VARIANT,

                    content = Column(
                        [
                            Text(self.title.title(), size=22, max_lines=1), 
                            Text("\n", size=2), 
                            Text("Date Added: " + self.date_added, size=8), 
                            Text("Target: " + self.target, size=8), 
                            Text("Progress: " + str(int(self.progress * 100)) + "%", size=8), 
                            Text("\n", size=1), 
                            ProgressBar(width=400, height=5, value=self.progress)
                        ],
                        spacing = 0,
                    ),
                    
                    alignment=alignment.top_left,
                    margin=5,
                    padding= padding.only(left=12, right=12, top=6),
                    width=300,
                    height=100,
                    border_radius=5,
                    ink=True,

                    on_click = self.check_goal if with_button else None
                )
        
            return x
        
        def delete_button(self, e):
            if self in long_goals:
                long_goals.remove(self)
                update_long_main()
            else:
                weekly_goals.remove(self)
                update_weekly_main()
            page.go("/")

        def delete_goal_screen(self, e):
            # Open GUI for the goal's detail
            delete_goal_contents.clear()
            delete_goal_contents.append(AppBar(title=Text(self.title), bgcolor=colors.SURFACE_VARIANT))
            delete_goal_contents.append(Text(value= "Are you sure you want to quit now? This can't be undone."))
            self.update_progress()
            if self.progress > 0:
                delete_goal_contents.append(Text(value= "You've already achieved " + str(int(self.progress * 100)) + "%" + " of the goal"))

            delete_goal_contents.append(ElevatedButton(text="Delete Anyway", on_click=self.delete_button, bgcolor=colors.RED, color=colors.WHITE))
            page.go("/delete_goal")
            
        def reset_screen(self, e):
            # Open GUI for the goal's detail
            reset_contents.clear()
            reset_contents.append(AppBar(title=Text(self.title), bgcolor=colors.SURFACE_VARIANT))
            reset_contents.append(Text(value= "Are you sure you want to reset all progress? This can't be undone."))

            reset_contents.append(ElevatedButton(text="Reset Anyway", on_click=self.reset_progress, bgcolor=colors.RED, color=colors.WHITE))
            page.go("/reset_progress")

        def add_subgoal_screen(self, e):
            page.go("/add_subgoal")

        def check_goal(self, e):
            # Open GUI for the goal's detail
            current_goal.clear()
            current_goal.append(self)
            current_goal[0].update_progress()

            check_goal_contents.clear()
            check_goal_contents.append(AppBar(title=Text(self.title), bgcolor=colors.SURFACE_VARIANT))
            check_goal_contents.append(self.to_display(False))
            check_goal_contents.append(Divider())
            self.update_time()
            check_goal_contents.append(Text(value="Total time required: " + str(self.time) + " days"))
            check_goal_contents.append(Divider())

            for i in self.subgoals:
                check_goal_contents.append(i.main_display())

            check_goal_contents.append(ElevatedButton(text="Add Subgoal", on_click=self.add_subgoal_screen))

            check_goal_contents.append(Divider())
            check_goal_contents.append(ElevatedButton(text="Reset Progress", on_click=self.reset_screen, bgcolor=colors.RED, color=colors.WHITE))

            if self.progress == 1.0:
                check_goal_contents.append(ElevatedButton(text="Clear Goal", on_click=self.delete_button, bgcolor=colors.GREEN, color=colors.WHITE))
            else:
                check_goal_contents.append(Container(
                    bgcolor=colors.RED_900,
                    content = Icon(icons.DELETE),

                    alignment=alignment.center,
                    width=120,
                    height=30,
                    border_radius=10, # rounded rectangle
                    ink=True,

                    on_click=self.delete_goal_screen
                ))
            page.go("/check_goal")

    page.title = "Subby"
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.window_width = 300
    page.window_height = 600
    page.scroll = ScrollMode.AUTO

    # -------------------------- CHECK / DELETE GOAL --------------------------

    check_goal_contents = []
    check_subgoal_contents = []
    delete_goal_contents = []
    reset_contents=[]
    reset_confirmation_screen_contents = []

    current_goal = []

    def add_subgoal(e):
        # Add error clauses


        result = SubGoal(sub_title.value, sub_note.value, sub_time.value, sub_point.value)

        current_goal[0].subgoals.append(result)

        # Reset all the inputs
        sub_title.value = ""
        # sub_target.value = ""
        sub_time.value = ""
        sub_note.value = ""
        sub_point.value = 1

        current_goal[0].check_goal(None)
        current_goal[0].update_progress()
        
        update_long_main()
        update_weekly_main()

        page.go("/check_goal")

    sub_contents = []

    sub_title = TextField(label="Title", capitalization = TextCapitalization.WORDS, max_length = 24)
    # sub_target = TextField(label="Target End Date", keyboard_type = KeyboardType.DATETIME, hint_text="YYYY/MM/DD")
    sub_time = TextField(label="Estimated Days Needed")
    sub_note = TextField(label="Extra Note", multiline=True)
    sub_point = Slider(min=1, max=10, divisions=9, label="{value}", value=1)

    sub_b = ElevatedButton(text="Submit", on_click=add_subgoal)

    sub_contents.append(AppBar(title=Text("Add Subgoal"), bgcolor=colors.SURFACE_VARIANT))
    sub_contents.append(sub_title)
    # sub_contents.append(sub_target)
    sub_contents.append(sub_time)
    sub_contents.append(sub_note)
    sub_contents.append(sub_point)
    sub_contents.append(sub_b)

    # -------------------------- ADD GOAL --------------------------

    def add_goal_screen(e):
        # Open GUI for making goal
        page.go("/add_goal")

    add_button = Container(
                bgcolor=colors.SURFACE_VARIANT,
                content = Icon(icons.ADD),

                alignment=alignment.center,
                margin=5,
                padding=20,
                width=300,
                height=65,
                border_radius=5, # rounded rectangle
                ink=True,

                on_click=add_goal_screen
            )

    # -------------------------- TAB 1 --------------------------
    long_goals = []
    page.client_storage.set("long_goals", long_goals)

    counter_long = Text(value= "Goal counts: " + str(len(long_goals)), text_align=TextAlign.RIGHT, width=100)

    long_main = []
    long_main.append(counter_long)

    for i in long_goals:
        long_main.append(i.to_display(True))

    long_main.append(add_button)

    tab_1 = Column(long_main, spacing=3, visible=True, horizontal_alignment = CrossAxisAlignment.CENTER, scroll=ScrollMode.AUTO)


    # -------------------------- TAB 2 --------------------------
    weekly_goals = []
    page.client_storage.set("weekly_goals", weekly_goals)

    counter_weekly = Text(value= "Goal counts: " + str(len(weekly_goals)), text_align=TextAlign.RIGHT, width=100)

    weekly_main = []
    weekly_main.append(counter_weekly)

    for i in weekly_goals:
        weekly_main.append(i.to_display(True))
    
    weekly_main.append(add_button)
    weekly_main.append(Divider())
    
        # -------------------------- RESET --------------------------

    def reset_all_weekly(e):
        for i in weekly_goals:
            i.reset_progress_all(None)
            i.update_progress()
        update_weekly_main()
        page.go("/")

    reset_confirmation_screen_contents.clear()
    reset_confirmation_screen_contents.append(AppBar(title=Text("Weekly Progress Reset"), bgcolor=colors.SURFACE_VARIANT))
    reset_confirmation_screen_contents.append(Text(value= "Reset all progress for the weekly tasks? This can't be undone."))

    reset_confirmation_screen_contents.append(ElevatedButton(text="Confirm", on_click=reset_all_weekly, bgcolor=colors.RED, color=colors.WHITE))

    def reset_confirmation_screen(e):
        page.go("/reset_all")

    reset_all = Container(
                bgcolor=colors.SURFACE_VARIANT,
                content = Text(value="Reset All Weekly Tasks"),

                alignment=alignment.center,
                margin=5,
                # padding=20,
                width=300,
                height=35,
                border_radius=5, # rounded rectangle
                ink=True,

                on_click=reset_confirmation_screen
            )

    weekly_main.append(reset_all)

    tab_2 = Column(weekly_main, spacing=3, visible=False, horizontal_alignment = CrossAxisAlignment.CENTER, scroll=ScrollMode.AUTO)


    # -------------------------- TAB 3 --------------------------
    tab_3 = Text("Tab 3",size=30,visible=False)

    tabs = [tab_1, tab_2, tab_3]

    # -------------------------- TAB NAVIGATOR --------------------------
    def changeTab(e):
        my_index = e.control.selected_index
        tabs[0].visible = True if my_index == 0 else False
        tabs[1].visible = True if my_index == 1 else False
        # tabs[2].visible = True if my_index == 2 else False
        page.update()

    nav = NavigationBar(
        bgcolor = "black",
        on_change = changeTab,
        selected_index=0,
        destinations=[
            NavigationDestination(icon=icons.EXPLORE, label="Long-term"),
            NavigationDestination(icon=icons.COMMUTE, label="Weekly"),
            # NavigationDestination(icon=icons.SETTINGS, label="Settings"),
        ]
    )


    # -------------------------- INPUT / OUTPUT --------------------------
    def update_long_main():
        page.client_storage.set("long_goals", long_goals)

        long_main.clear()
        counter_long = Text(value= "Goal counts: " + str(len(long_goals)), text_align=TextAlign.RIGHT, width=100)
        long_main.append(counter_long)
            
        for i in long_goals:
            long_main.append(i.to_display(True))

        long_main.append(add_button)

    def update_weekly_main():
        page.client_storage.set("weekly_goals", weekly_goals)

        weekly_main.clear()
        counter_weekly = Text(value= "Goal counts: " + str(len(weekly_goals)), text_align=TextAlign.RIGHT, width=100)
        weekly_main.append(counter_weekly)
            
        for i in weekly_goals:
            weekly_main.append(i.to_display(True))

        weekly_main.append(add_button)

        weekly_main.append(Divider())
        weekly_main.append(reset_all)
    
    def button_clicked(e):
        # Add error clauses


        result = Goal(title.value, target_end.value, note.value, long_term.value)

        if(long_term.value == True):
            long_goals.append(result)
            update_long_main()
            
            tabs[0] = Column(long_main, spacing=3, visible=True, horizontal_alignment = CrossAxisAlignment.CENTER, scroll=ScrollMode.AUTO)

            tabs[0].visible = True
            tabs[1].visible = False
            tabs[2].visible = False
            nav.selected_index=0
        
        else:
            weekly_goals.append(result)
            update_weekly_main()

            tabs[1] = Column(weekly_main, spacing=3, visible=True, horizontal_alignment = CrossAxisAlignment.CENTER, scroll=ScrollMode.AUTO)

            tabs[0].visible = False
            tabs[1].visible = True
            tabs[2].visible = False
            nav.selected_index=1

        # Reset all the inputs
        title.value = ""
        target_end.value = ""
        note.value = ""
        long_term.value = True

        page.go("/")

    input_contents = []

    title = TextField(label="Title", capitalization = TextCapitalization.WORDS, max_length = 24)
    target_end = TextField(label="Target End Date", keyboard_type = KeyboardType.DATETIME, hint_text="YYYY/MM/DD")
    note = TextField(label="Extra Note", multiline=True)
    long_term = Switch(label="Long Term", value=True)

    b = ElevatedButton(text="Submit", on_click=button_clicked)

    input_contents.append(AppBar(title=Text("Add Goal"), bgcolor=colors.SURFACE_VARIANT))
    input_contents.append(title)
    input_contents.append(target_end)
    input_contents.append(note)
    input_contents.append(long_term)
    input_contents.append(b)
    
    # -------------------------- POPUP NAVIGATOR --------------------------
    def route_change(route):
        if page.route == "/add_subgoal":
            page.views.append(
                View(
                    "/add_subgoal",
                    sub_contents,
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    padding=10,
                    spacing=20,
                    scroll=ScrollMode.AUTO
                )
            )
            page.update()
            return
        
        if page.route == "/check_subgoal":
            page.views.append(
                View(
                    "/check_subgoal",
                    check_subgoal_contents,
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    padding=10,
                    spacing=20,
                    scroll=ScrollMode.AUTO
                )
            )
            page.update()
            return

        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    Container(
                        content=Column(tabs, scroll=ScrollMode.AUTO),
                        ),
                    nav
                ],
                horizontal_alignment = CrossAxisAlignment.CENTER,
                scroll=ScrollMode.AUTO
            )
        )

        if page.route == "/add_goal":
            page.views.append(
                View(
                    "/add_goal",
                    input_contents,
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    padding=10,
                    spacing=20,
                    scroll=ScrollMode.AUTO
                )
            )
        
        if page.route == "/check_goal":
            page.views.append(
                View(
                    "/check_goal",
                    check_goal_contents,
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    padding=10,
                    spacing=5,
                    scroll=ScrollMode.AUTO
                )
            )

        if page.route == "/delete_goal":
            page.views.append(
                View(
                    "/delete_goal",
                    delete_goal_contents,
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    padding=10,
                    spacing=20,
                    scroll=ScrollMode.AUTO
                )
            )
        if page.route == "/reset_progress":
            page.views.append(
                View(
                    "/reset_progress",
                    reset_contents,
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    padding=10,
                    spacing=20,
                    scroll=ScrollMode.AUTO
                )
            )
        if page.route == "/reset_all":
            page.views.append(
                View(
                    "/reset_all",
                    reset_confirmation_screen_contents,
                    horizontal_alignment = CrossAxisAlignment.CENTER,
                    padding=10,
                    spacing=20,
                    scroll=ScrollMode.AUTO
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")

    print("TO DO: change dates to 3 different textboxes, conditions for the submits")

app(target=main)