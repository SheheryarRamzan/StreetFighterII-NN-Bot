Game bot is to be run by the same steps mentioned in the document.

1. For running a single bot (your bot vs CPU), open the single-player folder. For running two of your
bots at the same time both fighting each other, open the two-players folder.
2. Run EmuHawk.exe.
3. From File drop down, choose Open ROM. (Shortcut: Ctrl+O)
4. From the same single-player folder, choose the Street Fighter II Turbo (U).smc file.
5. From Tools drop down, open the Tool Box. (Shortcut: Shift+T)
6. Once you have performed the above steps, leave the emulator window and tool box open and open
the command prompt in the directory of the API and run the following commands:
For Python API: `python controller.py 1`
7. After executing the code, go and select your character(s) in the game after choosing normal mode.
Controls for selecting players can be set or seen from the controllers option in the config drop down
of the emulator.
8. Now click on the second icon in the top row (Gyroscope Bot). This will cause the emulator to
establish a connection with the program you ran and you will see "Connected to the game!" or
"CONNECTED SUCCESSFULLY" on the terminal.
9. If you have completed all of these steps successfully then you have successfully run the GameBot.
