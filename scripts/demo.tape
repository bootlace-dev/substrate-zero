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

# 1. View Interactive Main Menu & Architecture Pillars
Sleep 1s

# 2. Execute Chamber 8: The Compiler Assassin (Dead-Store Elimination)
Type "8"
Sleep 300ms
Enter
Sleep 1s

# Return to menu
Enter
Sleep 1s

# 3. Execute Chamber 5: Lattice Nonce Bias (Hidden Number Problem) LLL Heist
Type "5"
Sleep 300ms
Enter
Sleep 1s

# Return to menu
Enter
Sleep 1s

# Clean exit
Type "q"
Sleep 300ms
Enter
Sleep 500ms
