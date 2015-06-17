# tombola_python
Small Python interface with Tkinter to draw prices for a tombola 

## Still in development, use it wisely

I'll try to release an official version when I'll consider it finished, feel free to do modification and send pull requests

## How to use it
Run the gui.py script and the tool will open

The initialization is quite simple:
- First you need a csv file containing the people who participate to the tombola, the header of this csv shall be "Nom; Prenom" (see list_names_test.csv for example). To import it just click "Menu", "Importer joueurs" and select your file. You shall see that the "nombres de joueurs" has changed
- Secondly you need to import a csv file containing the list of prices, the header shall at list contain "Price" (see list_prices_tests.csv for example). To import it just click "Menu", "Importer prix" and select your file.
- Finally you can choose the interval duration between the draws and press "Lancer!"

The results of the tombola are stored in a csv file name save.csv, next to the script.

Enjoy
