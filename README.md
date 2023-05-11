# Model-Based-Testing-Of-The-Data-Plane
This Github page is for the master thesis "Model Based Testing for Programmable Data Planes" done at Luleå University of Technology

X7007E, Master Thesis in Computer Science and Engineering, Specialisation Information and Communication Technology

## Prerequisite
- [AltWalker](https://altwalker.github.io/altwalker/)
- [Mininet](https://github.com/mininet/mininet)
- [Bmw2](https://github.com/p4lang/behavioral-model)

## Usage
### Start mininet env
From the mininet folder run:
```
make startMininet
```
Then from another terminal run:
```
make popTable
make confVlan
```
This will populate the tables in the bmw2 switch.

### AltWalker
From the tests directory run:
```
runRand time=100
```
This will run AltWalker for 100 secounds.

## Author
- Gustav Rixon, Saab\LTU

## License
[GNU General Public License, version 2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html)
