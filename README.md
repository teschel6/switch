# switch

A cli tool used for organizing and quickly switching between active projects.
For those of use who just can't seem to work on one thing at a time.

Sometimes switching between projects isn't as simple as `cd` you may also
want to ...

- set environment variables
- start a container
- initalize a virtual environment
- activate a background process
- etc.

Use `switch` to easily create and manage startup scripts that get your terminal 
session and environment exactly how you need it for development. 

As a bonus this may also serve as documentation for local development setup.

# Usage - WIP

Brainstorming the usage of switch tool

```sh
# open a searchable list of projects to open
switch 

# open a project (with tab completion)
switch [project]

# initalize working directory as root of a new project
#  - creates .switch config file or directory
switch init

# add a project with and existing .switch config to your active projects
switch add

# open a searchable list of projects to remove
switch remove

# remove a project (with tab completion)
switch remove [project]

# open up the switch config file ~/.config/switch/config
switch config
```
