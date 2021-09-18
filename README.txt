ToDo is a student planner created to organize all the work, research, and tasks associated 
with any project in a single dashboard. It is meant to address inconveniences such as having
20+ tabs to keep track of between the start and end date of a project, keeping track of which
research links have been cited, keeping track of what tasks are left to accomplish for a 
project, and more. It would be a simple fix by just keeping this single tab open to keep track of all 
project progress.

ToDo contains a single app called Projects. It contains the following files:
1. Static files: the trash icon used, the logo, and a styles.css sheet that contains the 
stying for "layout.html".
2. Templates: There are six templates used in this project, two of which are utilized from
previous projects (login and register). There is a general layout template from which the others
extend which includes the top navbar, "index.html" which contains the view that lists a 
user's projects, "details.html" which contains the dashboard view of a project's details, and 
"lists.html" which contains the view of all the ToDo lists for a user.
3. "Admin.py" contains the configuration for the data models I would like to be able to access
through the admin interface.
4. "urls.py" contains the url paths for my project, each of which corresponds with a function in "views.py"
5. "models.py" contains four data models: User, Project, Link, and ToDo to store information about 
these structures.
The other files are standard and weren't modified much.

*Note: my Django framework isn't linking properly between separate javascript, CSS, and HTML files, so 
for this reason, the JS and CSS are written in the same document as the HTML, although this isn't best
practice*

I believe that my final project satisfies the complexity requirements as it provides many different
functionalities a student may find useful, including:
- creating a project and giving it relevant information such as name, class, due date, and being able
to view its completion status
- at the top of the details dashboard, being able to view relevant information quickly, including the 
info mentioned above as well as: number of days until due date, number of uncited sources remaining,
number of incomplete working documents remaining, and number of incomplete toDos remaining.
- adding research links identifiable by a link tag, stored in one place, and being able to quickly 
modify whether or not they are cited, or delete it easily.
- adding working document links identifiable by a tag (either a link or a file upload), and being able
to quickly modify whether or not they are completed, or delete it easily.
- adding toDo list items, and being able to quickly modify them once they are complete
- "Quick Search": putting a query into a search field and clicking a button which opens a tabl with a 
Google search or an EBSCO search of that query.
- having access to multiple other useful links by clicking buttons, including a thesaurus, dictionary,
and citation help
- being able to view and modify all your toDo lists in one independent view to see what work is left 
to be done.
- being able to move between different projects using the side navbar
- being able to complete a project, which removes the ability to edit anything on its details page as well
as removing the overview cards, but then reopen it if desired, which restores these abilities.

In addition, my project allows for multiple modifications of the view using JavaScript for user 
preference, including:
- hide/show completed projects
- hide/show completed toDo tasks
- collapse/expand toDo lists in the view of all the checklists

Finally, my project is mobile responsive, so if the window is made smaller or larger, the elements
adjust to fit in an aesthetic way. 

Thank you for checking out ToDo :)