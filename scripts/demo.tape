# Substrate Zero - Terminal Demo Tape
# Produces high-resolution hero demo for GitHub README
# Maintained by @bootlace-dev

Output "assets/demo.mp4"
Output "assets/demo.gif"

Set Shell "bash"
Set FontSize 12
Set FontFamily "JetBrains Mono, DejaVu Sans Mono, monospace"
Set Width 1220
Set Height 960
Set Padding 18
Set Theme "Catppuccin Mocha"
Set WindowBar "Rings"
Set TypingSpeed 30ms

Hide
Type "export PS1='bootlace@workstation:~/dev/substrate-zero$ '"
Enter
Type "cd /home/bootlace/dev/substrate-zero && clear"
Enter
Show

Sleep 500ms
Type "python3 -m substrate_zero.cli"
Sleep 300ms
Enter

# 1. View Interactive Main Menu & Architecture Pillars (Keys 1-9, A, Q)
Sleep 3s

# 2. Execute Option A: Run All Chambers Sequentially (Full Suite Chambers 1-9)
Type "A"
Sleep 500ms
Enter
Sleep 36s

# Return to menu
Enter
Sleep 3s

# Clean exit
Type "q"
Sleep 500ms
Enter
Sleep 2s
