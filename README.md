# switch

Switch is a cli tool used for organizing and quickly switching between active 
projects. For those of us who just can't seem to work on one thing at a time.

Use `switch` to easily create and manage projects in an IDE agnostic way ... 

- Create scripts that get your terminal session and environment exactly how 
you need it for development. 
- Open your project in your preferred editor/program.

# How it Works

Switch will create a project config file `.switch.toml` in each of your 
projects that you initialize. You can commit this file to your version control
system.

```toml
id = "01KBKBT1S9J55Z1FYNVNEHC3GH"
name = "switch"
activate = ["source", ".venv/bin/activate"]
```
Switch also creates a user config dotfile in your home directory, 
`~/.config/switch/config`. This contains references to all your projects as well
as any user config.

# Switch Quickstart 

```sh
# open help menu
switch --help
switch init --help

# initalize current working directory as new project
switch init

# initalize directory as root of a new project
switch init -d ~/git/my-project

# open a searchable list of projects to switch too
switch 

# add a project with and existing `.switch.toml` config
switch add

# remove a project from your user config
switch rm -d ~/git/sample-project

# open your user config file ~/.config/switch/config
switch config
```
