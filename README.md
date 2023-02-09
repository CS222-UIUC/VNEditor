## CS222 Project Draft 1

### Pitch

Today we have many webpage that supports the job of software like packing and unpacking file,transform `mp3` to `wav` file. We found it is hard to make a visual novel game without pre-installed software on the local computer this far. So an online visual novel game editor would greatly reduce the cost of creating a visual novel game.

### Functionality

1. Users can import the local file and developing process pack into the editor.

2. Users can pack and export the saving developing or developed file into the local.

3. Users can add text, into specific scene by importing file or typing.

4. Users can combine chatbox, character, sound, background into a scene.

5. Users can assign the sequence of scene to make a plot, if possible make different branch.

6. Users can edit character's animation in specific scene and the movement of camera

### Components

#### Backend

We will write the backend by using python with the fastapi framework. The reason we choose it is because all of our team member know how to coding in Python, and two of them have experience in building website (backend + frontend) by using web framework in Python. For our project, we do not need a lot of api but just some standard file io function. Hence, we choose to use `fastapi` as it can satisfied our requirement and can implement in a relatively fast way. The duty of the backend service is to provide our frontend a simpler way to manage the game resources, in our later iteration, we also plan to add a game save/load function in the executable file, which may require the backend write a simple PDO. All in all, our backend has following duty:

+ file IO: add, delete, modification, fetch
+ game memory PDO

#### Frontend

the major duty of our project is the frontend development, in order to finish our first demo in a faster way, we choose to use a popular frontend framework: `vue.js` as it can help us build a usable and pretty page in a comparably short time. Two of our team member have experience in  frontend development--bootstrap, and three of us know how to use javascript, so we plan to split the frontend task into four part so it will be easier for us to work together. The specified tasks are shown below:

+ top toolbar
+ middle preview bracket
+ left smaller preview bracket
+ right toolkit panel

![editor demo](doc/demo.png)

### Weekly Planning

1. Set up frontend with vue.js and backend with FastAPI, set up git repo and introduce basic workflow. Design basic UI features.
2. Allow user to add and delete frame. Only allow linear structure at this point. Allow images upload. Create clickable options to go to the next frame.
3. Allow creating and editing character and their associated text. Allow music upload. Creating UI for toolbar.
4. Allow stoping, inserting, and starting music. Allow the project to be "played". 
5. Allow a project to be saved and loaded in certain format. Continue to optimize UI.
6. Allow the project to be exported as a single executable file. Allow multiple branches following up a frame.
7. Start to create a demo using the editor. Allow the player to save their progress mid game.
8. Finish the demo.

### Potential Risks

[井盖]

### Teamwork [井盖]

[井盖]