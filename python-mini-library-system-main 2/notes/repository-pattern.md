# Repo
Repo = a place to store and organize the project code.
It also helps sharing work with the team.

When I open a repo, I usually check:
- what the project is about
- the main files/folders
- how to run it (README)
- any required notes/tasks I need to do


# Repository Pattern
Repository Pattern = keep reading/writing data in one place (repository layer),
so the rest of the app doesn’t deal with storage details.

Quick example in my head:
- App/Service = manager (borrow book / return book / register member)
- Repository = the employee who handles the archive
- Data source = the archive itself (JSON files / database)

So the manager tells the employee what to do, and the employee is the one who checks/updates the files.

How it works: Service → Repository → Data Source

In my Mini Library System, there are 3 parts:
1) Application/Service layer
   - library rules (is member found? is book found? is it available?)
   - should NOT open files or handle JSON directly

2) Repository layer
   - reading/saving data (load/save functions)
   - deals with JSON (or later a database)

3) Data source
   - the actual files:
     - books.json
     - members.json
     - loans.json

Why it’s useful:
- cleaner code (logic separated from data access)
- easier to change storage later (JSON \ DB)
- easier testing (can use a fake repository)
- less repeated file read/write code
