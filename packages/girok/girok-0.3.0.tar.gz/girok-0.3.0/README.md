<h1 align="center">✏️ Girok - The most powerful CLI task manager</h1>

[![Downloads](https://static.pepy.tech/badge/girok)](https://pepy.tech/project/girok)

<h3 align="center"> Who said you cannot have a beautiful UI on terminal?</h4>

<p align="center"><img src="/resources/girok-demo-transparent.gif"></img></center>

(p.s. No one said it to me)

# 💥 Introduction

**Girok**, which means "to record" in Korean, is a **powerful terminal-based task manager** which provides a multitude of scheduling operations that can be done in less than 10 seconds. It also supports **beautiful and responsive calendar GUI** in which you can move around with VIM key bindings.

# 💫 Highlighted Features

- Infinite recursive sub-categories with automatic assigned colors
- A beautiful and responsive calendar TUI(Termina User Interface)
- Add/Query a task super fast with a variety of date options

# 💬 Remarks

Girok works fluently with `MacOS` and `Linux` users. It also works with `Windows` but some features and UIs might break.

If you find it useful, consider supporting to help the development process! As I'm running the server with my own expense now, your help will make the service much more stable and fast!

If you want to see the server source code, go to [**girokserver**](https://github.com/noisrucer/girokserver).

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/changjin97z)

# 🤖 Version `0.2.5` is released now!

### Upgrade with `pip install girok --upgrade`

# 📖 Table of Contents

- [🚀 Installation](#-Installation)
- [🔥 Get Started !](#-get-started)
  - [🪟 0. Fancier UI](#fancierui)
    - [Contribute your background image!](#contributeimage)
  - [🙏 1. help command](#helpcommand)
  - [🔒 2. Registration](#register)
  - [🔓 3. Login / Logout](#loginandlogout)
  - [📚 4. Category commands](#categorycommands)
    - [4.1. `colors`](#colorscommand)
    - [4.2. `showcat`](#showcatcommand)
    - [4.3. `addcat`](#addcatcommand)
    - [4.4. `mvcat`](#mvcatcommand)
    - [4.5. `rmcat`](#rmcatcommand)
    - [4.6. `rncat`](#rncatcommand)
  - [📕 5. Task Commands](#taskcommands)
    - [5.1. `addtask`](#addtaskcommand)
    - [5.2. `showtask`](#showtaskcommand)
    - [5.3. `done`](#donecommand)
    - [5.4. `uptask`](#uptaskcommand)
  - [📅 6. Calendar Commands](#calendarcommands)
    - [6.1 Calendar Key Bindings](#movearoundcalendar)
    - [6.2 Calendar Demonstrations](#calendardemonstration)
- [🚒 Report Bugs](#-report-bugs)
- [😭 Uninstall](#-uninstall)
- [💌 Contributions](#-contributions)

# 🚀 Installation

Girok supports all operating systems including Linux, MacOS, Windows.

However, it works well on Unix-based shells such as `bash`, `zsh`, `fish`, `wsl`, etc.

Some shells like `powershell` might break some UIs.

Make sure you have Python `>=3.9` version installed.

To install,

```bash
pip install girok
```

Now you have installed `girok` on your machine. To make sure that it works, enter the following.

```bash
girok --help
```

Now, let's dive into Girok!

# 🔥 Get Started

## 🪟 0. Fancier UI <a name="fancierui"></a>

If you're a mac user (or other device supporting terminal transparency), **enhance your UI by setting up a (dark theme) background for your mac desktop** and **make it transparent!**

My settings are

1. `54 %` transparency
2. `20 %` opacity

The photo used in the demo: [dark-chinese-door](https://github.com/noisrucer/girok/tree/develop/background-images)

If you're an ITerm 2 user, for some weird reasons, the calendar doesn't apply the transparency. Please let me know if anyone figures this out to make it transparent for ITerm2! Please use the default mac terminal to see the change for the calendar.

If you have overflowing icons in the background, it looks bad. To hide the background icons(not deleting), enter the following command.

```bash
defaults write com.apple.finder CreateDesktop -bool false

killall Finder
```

To get back the icons, enter

```bash
defaults write com.apple.finder CreateDesktop -bool true; killall Finder
```

As I just found out about this transparency (and I'm lazy), I'll leave the below demonstrations as before. I'll update later.. :)

### Contribute your favorite background images! <a name="contributeimage"></a>

If you think your background image is awesome, you can contribute by sharing it with other people! Please visit the [detailed guide](https://github.com/noisrucer/girok/tree/develop/background-images/README.md).

## 🙏 1. Help command <a name="helpcommand"></a>

In order to see **all the commands** of **Girok**, enter `girok --help` in your terminal.

![alt text](images/girok2-help.png)

In order to see the details of each command, enter the following in your terminal.

```
girok <command> --help
```

For example, if you enter

```
girok addtask --help
```

then you'll see the following help message

![](images/girok2-command-help.png)


## 🔒 2. Registration <a name="register"></a>

To register a new account enter the following in your terminal.

```bash
girok register
```

![alt text](images/girok2-register.png)

1. Enter your email address to receive the verificaiton code
2. Check your email inbox and enter the verification code. If you can't find it, check junk email.
3. Finally enter your password to register. Note that password must be at least **7 characters** long and contain at least one **lowercase**, one **uppercase**, and one **special character** (`@`, `#`, `$`, `%`, `*`, `!`)


[WARNING] **Girok doesn't require you to enter your email service's password**. You can type any password as input.

Congratulations! Now let's go ahead and login to our account.

## 🔓 3. Login and Logout <a name="loginandlogout"></a>

In order to login, 

```bash
girok login
```

Now you're ready to use all the features!

## 📚 4. Category Commands <a name="categorycommands"></a>

You can pre-define **categories** such as `School`, `Life` and `Career` with automatically assigned category color.

Girok supports **infinite recursive subcategories**. All the subcategories will be assigned with the color of its topmost parent category.

Later on, you can link tasks to these categories.

### 4.1 `colors` command <a name="colorscommand"></a>

You can check out all the category colors with,

```bash
girok colors
```

![alt text](images/girok2-colors.png)

You can manually assign or update category color with the pre-defined color names.

### 4.2 `showcat` command <a name="showcatcommand"></a>

In order to see all the categories you have created, enter the following command.

```bash
girok showcat
```

![alt text](images/girok2-showcat.png)

### 4.3 `addcat` command <a name="addcatcommand"></a>

`addtask` command takes a single argument `category full path`.

In order to add a new category, enter the following command.

```bash
girok addcat <target path>
```

The `<target path>` is the **full path including the new category name**. For example, if you want to add a **topmost category** named `Career`, then enter

```bash
girok addcat Career
```

Then, you'll see the category tree with the newly created category being highlighted.

![alt text](images/girok2-addcat1.png)

In order to nest a sub-category under a previously defined category, pass the **FULL PATH** starting from the topmost category delimited by `/`, ending with the new category name.

For example, if you want to create a new category named `Resume` under the previously created `Career` category, enter the following command.

```bash
girok addcat Career/Resume
```

Then, you'll see `Resume` is created under `Career`.

![alt text](images/girok2-addcat2.png)

In this way, you can create as many categories and sub-categories as you want!

### 4.4 `mvcat` command <a name="mvcatcommand"></a>

Now you might want to move a category under another category.

In order to move a `category A` (recursively all its sub-categories) under `category B`, enter the following command.

```bash
girok mvcat <full path of A> <full path of B>
```

For example, if you want to move the whole `Career` category under `Dev/Network` (for some weird reason), enter the following command.

```bash
girok mvcat Career Dev/Network
```

![alt text](images/girok2-addcat4.png)

If you want to move a category to the `root category`, then pass `/` as the second argument. Let's move `Dev/Network/Career` back to the topmost category.

```bash
girok mvcat Dev/Network/Career /
```

![alt text](images/girok2-addcat5.png)

### 4.5 `rmcat` command <a name="rmcatcommand"></a>

Of course, you want to delete a category. In that case, enter the following command.

```bash
girok rmcat <full path of category>
```

Let's add a dummy category named `Dummy` under `Dev` then remove it.

As you already know, enter

```bash
girok addcat Career/Dummy
```

![](images/girok2-addcat6.png)

Now, let's delete it with the following command.

**[WARNING]** If you delete a category, **all its sub-categories and tasks will be DELETED**. I'll consider adding an option for users to preserve all the orphan tasks in the future. Please let me know in the issue if you need this feature!

```bash
girok rmcat Career/Dummy
```

Then, you'll be asked to confirm the deletion. Enter `y`.

![](images/girok2-rmcat1.png)

### 4.6 `upcat` command <a name="upcatcommand"></a>

You can update category information by

```bash
girok upcat -c <color> -n <name>
```

Note that the color must be one of the pre-defined colors from `girok colors` command.

Great job! Now let's move on to the task commands.

## 📕 5. Task commands <a name="taskcommands"></a>

**Girok** provides powerful task scheduling operations. You can perform different operations that would've taken a long time in other schedulers like Notion and Google Calendar in less than 10 seconds.

### 5.1 `addtask` command <a name="addtaskcommand"></a>

```bash
girok addtask <task name> [One of deadline date options] [-c | --category <category path>] [-p | --priority <priority>] [-t | --time <deadline time>] [-T | --tag <tag name>]

girok addtask <task name> -d <start date option>
```

#### 5.1.1 `addtask` rules

1. `<task name>` (Argument / **Required**)
   - If the task name has no space you can omit double quotes `""`. If it does, enclose it double quotes `""`
2. `-d | --date <date>@<time>` (Option / **Required**)
   - Start date and time (or deadline if end date is not present)
   - ex) `-d 5/18@17:50`, `-d 2025/8/15`, `-d tmr@17:30`, ...
   - The datetime value consists of `<date>` and `<time>`, concatenated by `@`. The `time` portion can be ommitted.
   - Allowed `<date>` values
      1. Explicit date: `-d 2024/5/19`
          - Specify an exact date delimited by `/`. You can enter the full date in the form of `yyyy/mm/dd`. Or, you can omit the year like `mm/dd` then the deadline year will be set to the current year.
          - You don't have to enter the exact form filled with `0`s. If the month is May, then just enter `5/23` or `05/23`.
      2. This week: `-d t1`
          - Sometimes, you're not aware of the exact date. If the date is some weekday of this week, you can just pass `t{1-7}` referrting to this monday to this sunday (monday indexed as `1`).
          - For example, if the deadline is this friday, enter `girok addtask "dummy" -d t5`
      3. Next week: `-d n1`
          - Similar to the above but referring to **next week**.
      4. After `N` days: `-d a10`
          - Sometimes, you process the deadline in your mind like "it's due 5 days later".
          - In this case, pass the number of days a task is due after.
          - For example, if the deadline is 5 days later, enter `girok addtask "dummy" -d a5`
      5. Today: `-d tdy|today`
      6. Tomorrow: `-d tmr|tomorrow`
    - Allowed `<time>` format
      - ex) `07:50`, `23:59`
      - You can also set the specific deadline time.
      - You must provide the full time format in **24 hour scale** such as `07:23` or `21:59`.
    - In summary, if you want to specify the full date as well as the time, you can do so by `girok addtask "Submit assignment" -d tmr@23:59`
3. `-e | --end <date>@<time>` (Option, **Optional**)
    - If your task is spanning on multiple days, you can also specify the end date
    - The format is the same as `-d` option.
4. `-r | --repetition <daily | weekly | monthly | yearly>` (Option / **Optional**)
    - You can also specify a recurring task using `-r` option.
    - The repetition type must be one of `daily`, `weekly`, `monthly`, `yearly`.
    - **Only single-day task** can be recurring. Recall that we have two datetime options: `-d`, `-e` and each consists of "date" and "time". Let's define them `start date`, `start time`, `end date`, `end time`. Then, only the following combinations(single-day task) are allowed for repetition.
        1. `start date` only
        2. `start date`, `start time` only
        3. `start date`, `start time`, `end date`, `end time` only, and `start date == end date`
    - The start day of the recurring event is automatically set to the `start date` you specified with `-d` option.
4. `-c | --category <category full path>` (Option / **Optional**)
   - Your tasks might belong to a specific category you have previously defined.
   - Provide the **full category path**.
   - For example, if your task belongs to `Career/Resume`, then enter `girok addtask "dummy task 1" -d tmr -c Career/Resume`.
   - If you specify a category, then the task color will be automatically linked to that category's color.
   - If no category is provided, the task will belong to `No Category` category.
5. `-p | --priority <low | medium | high>` (Option, **Optional**)
   - You can set the priority of a task so that you can filter out by priority when you query your tasks.
   - For example, to set the priority of a task as `low`, enter `girok addtask "dummy task 1" -d tmr -p low`.
6. `-t | --tag <tag name>` (Option, **Optional**)
   - You can set the **tag** of a task such as `assignment` and `meeting`. With tags, you can more efficiently query your tasks with different types.
   - Unlike category, tag doesn't allow nested tags and you don't have to pre-define them.
   - For example, if you want to set the tag of a task as `assignment`, enter `girok addtask "assignment 4" -d 4/24 -t assignment`
7. `-m | --memo <memo>`
   - You can also add a memo for your task with `-m `option
   - ex) `girok addtask "Meeting with Jason" -d tmr -m "don't forget to prepare the documents"`

In summary, keep the following rules in mind.

1. Always provide **task name** and `-d` option.
2. Although not required, it's better to provide **category** to manage your tasks more effectively.
3. Other options are up to you.

For example, the following command is a typical command that I use on everyday basis.

```bash
girok addtask "Implement tag filtering feature" -c Dev/Girok -d n3 -p high
```

It looks quite complicated, but you'll get used to it quickly after playing out a little bit.

#### 5.1.2 `addtask` demonstration

Now let's play around with `addtask` command.

Suppose our category list is

![alt text](images/girok2-addtask-demon1.png)

In the demonstration, I will add several tasks and show how it works.

Let's add a task named `go over resume again` whose category is `Career/Resume` and I will do it by `next thursday`. This is a quite important task, so I will assign the `priority` high.

```bash
girok addtask "go over resume again" -c Career/Resume -d n4 -p high
```

![alt text](images/girok2-addtask-demon2.png)


Now I'll add another task named `Midterm exam` with the category `HKU/COMP3234` and it's a 3-day exam from `4/18 09:30 AM` to `4/20 10:00`. Let's also add `exam` tag and memo.

```bash
girok addtask "Midterm exam" -c HKU/COMP3234 -d 4/18@09:30 -e 4/20@10:00 -t exam -m "Do not forget to bring cheatsheet"
```

![alt text](images/girok2-addtask-demon3.png)


Lastly, I'll add a task named `Gym day` and I will go every day at 7 AM in the morning.

```bash
girok addtask "Gym day" -d tmr@07:00 -r daily
```

![alt text](images/girok2-addtask-demon4.png)


### 5.2 `showtask` command. <a name="showtaskcommand"></a>

```bash
girok showtask [--tree] Deadline date options] [-c | --category <category path>] [-p | --priority <priority>] [-T | --tag <tag name>]
```

Girok provides powerful commands to effectively query your schedule with many different options. You can filter tasks by category, priority, deadline, and tag.

#### 5.2.1 Table view vs Tree view

You can type `girok showtask` command with no parameter. The default view of the command is **table view**.

Note that I've added some more tasks to make the visualization rich.

```bash
girok showtask
```

![](images/girok2-showtask1.png)

By default, all tasks will be shown in a nice table format.

If you want to view your tasks in a tree view, then provide `--tree` flag.

```bash
girok showtask --tree
```

![](images/girok2-showtask2.png)

#### 5.2.2 Filter by date options

You can query your tasks filtering by many different date options. Notice that all the options for `showtask` command are optional.

1. `-e | --exact <date format from addtask -d option>`
   - To view tasks due to a specific day, provide the exact date after the flag
2. `-d | --day <# days>`
   - To view tasks due **within `n` days**, provide the number of days `n` after the flag
3. `-w | --week <# days>`
   - To view tasks due **within `n` weeks**, provide the number of weeks `n` after the flag
4. `-m | --month <# days>`
   - To view tasks due **within `n` months**, provide the number of months `n` after the flag
5. `--tdy`
   - To view tasks due today.
6. `--tmr`
   - To view tasks due within tomorrow (today && tomorrow)
7. `--tw`, `--nw`
   - To view tasks due within this week and next week, respectively
8. `--tm`, `--nm`
   - To view tasks due within this month and next month, respectively
9. `-u | --urgent`
   - To view urgent tasks that are within `3 days` by default

#### 5.2.3 Filter by category

To query tasks under a specific category, use the following command,

```bash
girok showtask [-c | --category] <category path>
```

For example, to query tasks only for the `HKU` category. Enter the following command.

```bash
girok showtask -c HKU
```

or

```bash
girok showtask -c HKU --tree # tree view
```

![](images/girok2-showtask3.png)


#### 5.2.4 Filter by priority

```bash
girok showtask [-p | --priority] <low | medium | high>
```

To view tasks with a specific priority, provide `-p` option followed by the priority number between `1` and `5`.

For example, to view tasks with priority 5, enter the following command

```bash
girok showtask -p 5
```

#### 5.2.5 Filter by tag

```
girok showtask [-t | --tag] <tag name>
```

### 5.3 `done` command <a name="donecommand"></a>

To complete(delete) a task, provide the `done` command followed by the task ID.

Optionally, you can pass `-y` or `--yes` flag if you don't want to see the confirmation message.

```
girok done <task ID> [-y | --yes]
```

**[IMPORTANT]** The **TASK ID** is the IDs you can see when you perform `showtask` operations. Note that the **ONLY the Task IDs of the LATEST showtask operation are valid**. In other words, if you consecutively type `girok showtask` and `girok showtask -p 5` but try to delete a task with the task IDs shown in the table of the first `girok showtask` command, you might delete an unexpected task!!

For example, suppose you enter `girok showtask` command.

![alt text](images/girok2-done1.png)

If you completed the task `Hangout with Jason`, provide the task ID at the leftmost column.

```bash
girok done 3
```

### 5.4 `uptask` command <a name="uptaskcommand"></a>

You can update task information with `giork uptask` command.

```bash
girok chdate <taskID> -n <name> -d <start datetime> -e <end datetime> -r <repetition type> -c <category> -t <tag> -p <priority> -m <memo>
```

Note that the start and end datetime format are the same as the one from `-d` option of `addtask` command.

## 📅 6. Calendar Commands <a name="calendarcommands"></a>

The beauty of **Girok** is the **beautiful and responsive full calendar GUI**.

![](images/girok-cal1.png)

To fire up the calendar, enter the following command

```
girok cal
```

Then you'll be prompted to the calendar GUI.

**girokcal** offers a beautiful but minimalistic GUI in which you can move around with (not exactly same but similar) **VIM key bindings**.

Notice that all the categories and tags we have created so far are linked to the **sidebar**.

### 6.1 Calendar Key Bindings <a name="movearoundcalendar"></a>

![](images/girok-cal8.png)

Upon `girok cal` command, the starting **"focus"** is the **category tree**.

- Select a category/tag
  - `o` - select the current category/tag
- Move inside **category tree** or **tag tree**
  - `j` - down
  - `k` - up
- Move from **category tree** to **tag tree**
  - `ctrl + j`
- Move from **tag tree** to \*\_category tree
  - `ctrl + k`
- Moving from **category tree** or **tag tree** to **calendar**
  - `e`
- Moving from **calendar** to back **sidebar** (to category tree by default)
  - `w`
- Move inside the **calendar**
  - `h` - left
  - `j` - down
  - `k` - up
  - `l` - right
- Select a **calendar cell** (day) to view details
  - `o` - select the currently focused calendar cell
- **Next month**
  - `i`
- **Previous month**
  - `u`
- **Direct to the current month**
  - `y`
- **Toggle side bar**
  - `f`
- **Close calendar**
  - `q`

### 6.2 Calendar Demonstrations <a name="calendardemonstration"></a>

When you click on a category, then the category title will change accordingly at the left-bottom corner of the calendar. All the tasks belonging to the selected category will be shown.

Let's select `HKU` category by pressing alphabet `o` key.

![](images/girok-cal4.png)

Notice that only the tasks with the yellow dots (HKU category color) are shown.

Now let's select `All Categories` and change our focus from the **category tree** to the **tag tree** by pressing `ctrl+j` key. Then, select `exam` tag.

![](images/girok-cal5.png)

Yay! I don't have any exams this month.

But.. do I have exams next month? To check it out, let's press `i` to move to the next month.

![](images/girok-cal6.png)

Lastly, let's press `f` to close the sidebar to have make the calendar bigger.

![](images/girok-cal7.png)

Great job! Now, it's time to explore all the features of **Girok** on your own!!

# 🚒 Report Bugs

The first version of **Girok** was released just a couple days ago so you might encounter some bugs and errors.

If so, I'd greatly appreciate if you report them as raising `issues` then I will respond and update as soon as possible!!

# 😭 Uninstall

I'm sorry that there's no way to uninstall this package.

Just kidding. Enter `pip uninstall girok` in your terminal. Bye..😢

# 💌 Contribute to the project

- If you have any new features that would make your life easier, please don't hesitate to raise issues.

- If you wish to contribute to the project as a programmer, please first **open an issue** with the `feature` tag (title prefixed with `[Feat] description`) describing your suggested features. After getting approval from the maintainer, you can drop pull requests and I will review each of them carefully.
