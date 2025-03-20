<span id='projectdescription'></span>
## Project description
Stay out of <i>debug hell</i> by letting the `mutationtracker` do the dirty work for you! It will ease up the process
of identifying where an object took a wrong turn.
Just don’t tell your employer, so they won’t fire half your colleagues due to the time saved on debugging.

### Features
* Hold all mutations in the `MutationLedger` in the `MUTATIONS` attribute of any child class of `MutationTrackedObject` 
or class decorated by `track_mutations` (includes full trace stack)
* Log creation and mutations of object with log callable of your choice (e.g. `print`, `logger.debug`, `logger.info`)
* If a `MutationTrackedObject` is set as attribute value to another `MutationTrackedObject`, the caller function of the 
'filler' is saved in the `filled_by` attribute of the `MutationLedger` 

## Table of contents
* <a href='#projectdescription'>Project description</a>
* <a href='#howto'>How to install & use</a>
* <a href='#example1'>Example 1: MutationTrackedObject base class</a>
* <a href='#example2'>Example 2: track_mutations decorator</a>
* <a href='#limitations'>Limitations</a>
* <a href='#releasenotes'>Release notes</a>
* <a href='#hyperlinks'>Useful links</a>
* <a href='#license'>License</a>

## How to install & use
Install this package easily using pip:

```commandline
pip install mutationtracker
```

This project aims to be very easy to use. Import either the `MutationTrackedObject` or `track_mutations` decorator in 
your Python module. Next, define your custom class of which instances should be tracked, and optionally add a log 
callable to it:

```Python
from mutationtracker import MutationTrackedObject


class YourClass(MutationTrackedObject):
    _mutations_log_function = print  # optional attribute; might be other callable; default is no logging

    def __init__(self):
        ...
```
or
```Python
from mutationtracker import track_mutations


@track_mutations(log_function=print)  # optional keyword argument; might be other callable; default is no logging
class YourClass:
    def __init__(self):
        ...
```
Your class will automatically contain the `MUTATIONS` attribute holding the full mutation history of the instance. 
For an extensive enjoyable example, try <a href='#example1'>code below.</a>

<span id='example1'></span>
## Example 1: MutationTrackedObject base class
### Code
This example is best shown using two files in a single directory: `alice_and_bob.py` and `run.py`. The latter is not 
mandatory, but will improve the result because it not ran as script. Let's create `alice_and_bob.py` first with the 
following contents:
```Python
from datetime import datetime, date
import time

from mutationtracker import MutationTrackedObject


class Person(MutationTrackedObject):

    _mutations_log_function = print  # optional attribute, remove for no console output

    def __init__(
        self,
        social_security_number,
        name,
        gender,
        date_of_birth,
        children,
        date_of_death=None,
    ):
        self.social_security_number = social_security_number
        self.name = name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.date_of_death = date_of_death
        self.children = children

    def have_child(
        self, social_security_number, name, gender, date_of_birth=datetime.now().date()
    ):
        baby = Person(social_security_number, name, gender, date_of_birth, [])
        self.children = self.children + [baby]

    def adopt_child(
        self, social_security_number, name, gender, date_of_birth=datetime.now().date()
    ):
        child = Person(social_security_number, name, gender, date_of_birth, [])
        self.children = self.children + [child]

    def __repr__(self):
        return f"{self.social_security_number} - {self.name}"


def main():
    #  ========== Example: init of Alice ==========
    print("========== Example: init of Alice ==========")
    example_person = Person(12345678901, "Alice", "Female", date(1990, 3, 7), [])

    #  ========== Example: children ==========
    print("\n========== Example: children ==========")
    #  might one day have children herself
    example_person.have_child(12312312301, "Charles", "Male")
    example_person.have_child(12312312302, "Davey", "Male")
    #  might also adopt one more
    example_person.adopt_child(
        99889988771, "Fatima", "Female", date_of_birth=date(2024, 2, 2)
    )
    #  might find out Charles is actually a different baby because of a hospital mix-up
    #  so put him up for adoption as he is not as enjoyable

    def get_rid_of_child(person, name):
        person.children = [c for c in person.children if c.name != name]

    get_rid_of_child(example_person, "Charles")

    #  ========== Example: gender ==========
    print("\n========== Example: gender ==========")
    #  is her gender right? might change

    def change_gender(person, new_name, new_gender):
        """Might one day find out something is off but that can be changed"""
        time.sleep(0.1)  # takes some time
        person.name = new_name
        person.gender = new_gender

    #  actually, she feels like he and continues as Bob
    change_gender(example_person, "Bob", "Male")
    #  Might regret that later, and actually convert back
    change_gender(example_person, "Alice", "Female")

    #  ========== Example: safari trip gone wrong ==========
    print("\n========== Example: safari trip gone wrong ==========")
    #  live is an adventure, so go on a nice safari trip

    def go_on_safari(person):
        """Go on a nice and safe safari trip, so better be careful, right?"""
        pet_lion(person)

    def pet_lion(person):
        """Do not try this at home, or at the zoo, or while on safari, or anywhere ever, it might end badly"""
        person.date_of_death = datetime.now().date()

    go_on_safari(example_person)

    #  ========== Example: log full history of Alice ==========
    print("\n========== Example: log full history of Alice ==========")
    example_person.log_all_mutations()

    return example_person


if __name__ == "__main__":
    main()

```
Next up, you might want to create `run.py` to prevent it from running as script:
```Python
from alice_and_bob import main

"""
This example shows the Person class with baseclass MutationTrackedObject, and tells the life story of instance Alice

Make sure to put an breakpoint on the line with the `print` function and take a look at
`example_person.MUTATIONS` for the full experience provided by the MutationTrackedObject baseclass
"""
example_person = main()

# place a breakpoint on the print() line below
# run it in debug mode
# and make sure to check out example_person.MUTATIONS for the full experience
print("Thank you for trying the example with the baseclass MutationTrackedObject!")

```
### Output
```
========== Example: init of Alice ==========
A new Person instance is being created by examples.baseclass.alice_and_bob.main:46: args=(12345678901, 'Alice', 'Female', datetime.date(1990, 3, 7), []), kwargs={}
Change in Person instance (repr unavailable) attribute social_security_number: to 12345678901 from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:20)
Change in Person instance (repr unavailable) attribute name: to Alice from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:21)
Change in Person instance (12345678901 - Alice) attribute gender: to Female from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:22)
Change in Person instance (12345678901 - Alice) attribute date_of_birth: to 1990-03-07 from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:23)
Change in Person instance (12345678901 - Alice) attribute date_of_death: to None from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:24)
Change in Person instance (12345678901 - Alice) attribute children: to [] from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:25)

========== Example: children ==========
A new Person instance is being created by examples.baseclass.alice_and_bob.Person.have_child:30: args=(12312312301, 'Charles', 'Male', datetime.date(2025, 3, 16), []), kwargs={}
Change in Person instance (repr unavailable) attribute social_security_number: to 12312312301 from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:20)
Change in Person instance (repr unavailable) attribute name: to Charles from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:21)
Change in Person instance (12312312301 - Charles) attribute gender: to Male from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:22)
Change in Person instance (12312312301 - Charles) attribute date_of_birth: to 2025-03-16 from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:23)
Change in Person instance (12312312301 - Charles) attribute date_of_death: to None from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:24)
Change in Person instance (12312312301 - Charles) attribute children: to [] from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:25)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles] from [] (by examples.baseclass.alice_and_bob.Person.have_child:31)
A new Person instance is being created by examples.baseclass.alice_and_bob.Person.have_child:30: args=(12312312302, 'Davey', 'Male', datetime.date(2025, 3, 16), []), kwargs={}
Change in Person instance (repr unavailable) attribute social_security_number: to 12312312302 from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:20)
Change in Person instance (repr unavailable) attribute name: to Davey from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:21)
Change in Person instance (12312312302 - Davey) attribute gender: to Male from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:22)
Change in Person instance (12312312302 - Davey) attribute date_of_birth: to 2025-03-16 from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:23)
Change in Person instance (12312312302 - Davey) attribute date_of_death: to None from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:24)
Change in Person instance (12312312302 - Davey) attribute children: to [] from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:25)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles, 12312312302 - Davey] from [12312312301 - Charles] (by examples.baseclass.alice_and_bob.Person.have_child:31)
A new Person instance is being created by examples.baseclass.alice_and_bob.Person.adopt_child:36: args=(99889988771, 'Fatima', 'Female', datetime.date(2024, 2, 2), []), kwargs={}
Change in Person instance (repr unavailable) attribute social_security_number: to 99889988771 from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:20)
Change in Person instance (repr unavailable) attribute name: to Fatima from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:21)
Change in Person instance (99889988771 - Fatima) attribute gender: to Female from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:22)
Change in Person instance (99889988771 - Fatima) attribute date_of_birth: to 2024-02-02 from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:23)
Change in Person instance (99889988771 - Fatima) attribute date_of_death: to None from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:24)
Change in Person instance (99889988771 - Fatima) attribute children: to [] from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:25)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles, 12312312302 - Davey, 99889988771 - Fatima] from [12312312301 - Charles, 12312312302 - Davey] (by examples.baseclass.alice_and_bob.Person.adopt_child:37)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312302 - Davey, 99889988771 - Fatima] from [12312312301 - Charles, 12312312302 - Davey, 99889988771 - Fatima] (by examples.baseclass.alice_and_bob.get_rid_of_child:61)

========== Example: gender ==========
Change in Person instance (12345678901 - Alice) attribute name: to Bob from Alice (by examples.baseclass.alice_and_bob.change_gender:72)
Change in Person instance (12345678901 - Bob) attribute gender: to Male from Female (by examples.baseclass.alice_and_bob.change_gender:73)
Change in Person instance (12345678901 - Bob) attribute name: to Alice from Bob (by examples.baseclass.alice_and_bob.change_gender:72)
Change in Person instance (12345678901 - Alice) attribute gender: to Female from Male (by examples.baseclass.alice_and_bob.change_gender:73)

========== Example: safari trip gone wrong ==========
Change in Person instance (12345678901 - Alice) attribute date_of_death: to 2025-03-16 from None (by examples.baseclass.alice_and_bob.pet_lion:90)

========== Example: log full history of Alice ==========
===== All mutations for Person instance 12345678901 - Alice =====
Created by: examples.baseclass.alice_and_bob.main:46
Last mutation by: examples.baseclass.alice_and_bob.pet_lion:90
Filled by: None
Number of attribute mutations: 15
Change in Person instance (12345678901 - Alice) attribute social_security_number: to 12345678901 from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:20)
Change in Person instance (12345678901 - Alice) attribute name: to Alice from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:21)
Change in Person instance (12345678901 - Alice) attribute gender: to Female from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:22)
Change in Person instance (12345678901 - Alice) attribute date_of_birth: to 1990-03-07 from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:23)
Change in Person instance (12345678901 - Alice) attribute date_of_death: to None from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:24)
Change in Person instance (12345678901 - Alice) attribute children: to [] from AttributeDoesNotExist (by examples.baseclass.alice_and_bob.Person.__init__:25)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles] from [] (by examples.baseclass.alice_and_bob.Person.have_child:31)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles, 12312312302 - Davey] from [12312312301 - Charles] (by examples.baseclass.alice_and_bob.Person.have_child:31)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles, 12312312302 - Davey, 99889988771 - Fatima] from [12312312301 - Charles, 12312312302 - Davey] (by examples.baseclass.alice_and_bob.Person.adopt_child:37)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312302 - Davey, 99889988771 - Fatima] from [12312312301 - Charles, 12312312302 - Davey, 99889988771 - Fatima] (by examples.baseclass.alice_and_bob.get_rid_of_child:61)
Change in Person instance (12345678901 - Alice) attribute name: to Bob from Alice (by examples.baseclass.alice_and_bob.change_gender:72)
Change in Person instance (12345678901 - Alice) attribute gender: to Male from Female (by examples.baseclass.alice_and_bob.change_gender:73)
Change in Person instance (12345678901 - Alice) attribute name: to Alice from Bob (by examples.baseclass.alice_and_bob.change_gender:72)
Change in Person instance (12345678901 - Alice) attribute gender: to Female from Male (by examples.baseclass.alice_and_bob.change_gender:73)
Change in Person instance (12345678901 - Alice) attribute date_of_death: to 2025-03-16 from None (by examples.baseclass.alice_and_bob.pet_lion:90)
Thank you for trying the example with the baseclass MutationTrackedObject!
```
### Debug mode
Feel free to experience it yourself in debug mode to explore the data in `example_person.MUTATIONS` near the end of the 
example script. There's more data than printed in the log, such as the full trace stack. 

<span id='example2'></span>
## Example 2: track_mutations decorator
### Code
This example is best shown using two files in a single directory: `alice_and_bob.py` and `run.py`. The latter is not 
mandatory, but will improve the result because it not ran as script. Let's create `alice_and_bob.py` first with the 
following contents:
```Python
from datetime import datetime, date
import time

from mutationtracker import track_mutations


@track_mutations(log_function=print)  # optional keyword argument, default: no output
class Person:
    def __init__(
        self,
        social_security_number,
        name,
        gender,
        date_of_birth,
        children,
        date_of_death=None,
    ):
        self.social_security_number = social_security_number
        self.name = name
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.date_of_death = date_of_death
        self.children = children

    def have_child(
        self, social_security_number, name, gender, date_of_birth=datetime.now().date()
    ):
        baby = Person(social_security_number, name, gender, date_of_birth, [])
        self.children = self.children + [baby]

    def adopt_child(
        self, social_security_number, name, gender, date_of_birth=datetime.now().date()
    ):
        child = Person(social_security_number, name, gender, date_of_birth, [])
        self.children = self.children + [child]

    def __repr__(self):
        return f"{self.social_security_number} - {self.name}"


def main():
    #  ========== Example: init of Alice ==========
    print("========== Example: init of Alice ==========")
    example_person = Person(12345678901, "Alice", "Female", date(1990, 3, 7), [])

    #  ========== Example: children ==========
    print("\n========== Example: children ==========")
    #  might one day have children herself
    example_person.have_child(12312312301, "Charles", "Male")
    example_person.have_child(12312312302, "Davey", "Male")
    #  might also adopt one more
    example_person.adopt_child(
        99889988771, "Fatima", "Female", date_of_birth=date(2024, 2, 2)
    )
    #  might find out Charles is actually a different baby because of a hospital mix-up
    #  so put him up for adoption as he is not as enjoyable

    def get_rid_of_child(person, name):
        person.children = [c for c in person.children if c.name != name]

    get_rid_of_child(example_person, "Charles")

    #  ========== Example: gender ==========
    print("\n========== Example: gender ==========")
    #  is her gender right? might change

    def change_gender(person, new_name, new_gender):
        """Might one day find out something is off but that can be changed"""
        time.sleep(0.1)  # takes some time
        person.name = new_name
        person.gender = new_gender

    #  actually, she feels like he and continues as Bob
    change_gender(example_person, "Bob", "Male")
    #  Might regret that later, and actually convert back
    change_gender(example_person, "Alice", "Female")

    #  ========== Example: safari trip gone wrong ==========
    print("\n========== Example: safari trip gone wrong ==========")
    #  live is an adventure, so go on a nice safari trip

    def go_on_safari(person):
        """Go on a nice and safe safari trip, so better be careful, right?"""
        pet_lion(person)

    def pet_lion(person):
        """Do not try this at home, or at the zoo, or while on safari, or anywhere ever, it might end badly"""
        person.date_of_death = datetime.now().date()

    go_on_safari(example_person)

    #  ========== Example: log full history of Alice ==========
    print("\n========== Example: log full history of Alice ==========")
    example_person.log_all_mutations()

    return example_person


if __name__ == "__main__":
    main()

```
Next up, you might want to create `run.py` to prevent it from running as script:
```Python
from alice_and_bob import main

"""
This example shows the Person class with decorator track_mutations, and tells the life story of instance Alice

Make sure to put an breakpoint on the line with the `print` function and take a look at
`example_person.MUTATIONS` for the full experience provided by the track_mutations decorator
"""
example_person = main()


# place a breakpoint on the print() line below
# run it in debug mode
# and make sure to check out example_person.MUTATIONS for the full experience
print("Thank you for trying the example with the decorator track_mutations!")

```
### Output
```
========== Example: init of Alice ==========
A new Person instance is being created by examples.decorator.alice_and_bob.main:44: args=(12345678901, 'Alice', 'Female', datetime.date(1990, 3, 7), []), kwargs={}
Change in Person instance (repr unavailable) attribute social_security_number: to 12345678901 from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:18)
Change in Person instance (repr unavailable) attribute name: to Alice from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:19)
Change in Person instance (12345678901 - Alice) attribute gender: to Female from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:20)
Change in Person instance (12345678901 - Alice) attribute date_of_birth: to 1990-03-07 from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:21)
Change in Person instance (12345678901 - Alice) attribute date_of_death: to None from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:22)
Change in Person instance (12345678901 - Alice) attribute children: to [] from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:23)

========== Example: children ==========
A new Person instance is being created by examples.decorator.alice_and_bob.Person.have_child:28: args=(12312312301, 'Charles', 'Male', datetime.date(2025, 3, 16), []), kwargs={}
Change in Person instance (repr unavailable) attribute social_security_number: to 12312312301 from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:18)
Change in Person instance (repr unavailable) attribute name: to Charles from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:19)
Change in Person instance (12312312301 - Charles) attribute gender: to Male from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:20)
Change in Person instance (12312312301 - Charles) attribute date_of_birth: to 2025-03-16 from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:21)
Change in Person instance (12312312301 - Charles) attribute date_of_death: to None from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:22)
Change in Person instance (12312312301 - Charles) attribute children: to [] from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:23)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles] from [] (by examples.decorator.alice_and_bob.Person.have_child:29)
A new Person instance is being created by examples.decorator.alice_and_bob.Person.have_child:28: args=(12312312302, 'Davey', 'Male', datetime.date(2025, 3, 16), []), kwargs={}
Change in Person instance (repr unavailable) attribute social_security_number: to 12312312302 from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:18)
Change in Person instance (repr unavailable) attribute name: to Davey from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:19)
Change in Person instance (12312312302 - Davey) attribute gender: to Male from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:20)
Change in Person instance (12312312302 - Davey) attribute date_of_birth: to 2025-03-16 from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:21)
Change in Person instance (12312312302 - Davey) attribute date_of_death: to None from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:22)
Change in Person instance (12312312302 - Davey) attribute children: to [] from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:23)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles, 12312312302 - Davey] from [12312312301 - Charles] (by examples.decorator.alice_and_bob.Person.have_child:29)
A new Person instance is being created by examples.decorator.alice_and_bob.Person.adopt_child:34: args=(99889988771, 'Fatima', 'Female', datetime.date(2024, 2, 2), []), kwargs={}
Change in Person instance (repr unavailable) attribute social_security_number: to 99889988771 from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:18)
Change in Person instance (repr unavailable) attribute name: to Fatima from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:19)
Change in Person instance (99889988771 - Fatima) attribute gender: to Female from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:20)
Change in Person instance (99889988771 - Fatima) attribute date_of_birth: to 2024-02-02 from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:21)
Change in Person instance (99889988771 - Fatima) attribute date_of_death: to None from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:22)
Change in Person instance (99889988771 - Fatima) attribute children: to [] from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:23)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles, 12312312302 - Davey, 99889988771 - Fatima] from [12312312301 - Charles, 12312312302 - Davey] (by examples.decorator.alice_and_bob.Person.adopt_child:35)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312302 - Davey, 99889988771 - Fatima] from [12312312301 - Charles, 12312312302 - Davey, 99889988771 - Fatima] (by examples.decorator.alice_and_bob.get_rid_of_child:59)

========== Example: gender ==========
Change in Person instance (12345678901 - Alice) attribute name: to Bob from Alice (by examples.decorator.alice_and_bob.change_gender:70)
Change in Person instance (12345678901 - Bob) attribute gender: to Male from Female (by examples.decorator.alice_and_bob.change_gender:71)
Change in Person instance (12345678901 - Bob) attribute name: to Alice from Bob (by examples.decorator.alice_and_bob.change_gender:70)
Change in Person instance (12345678901 - Alice) attribute gender: to Female from Male (by examples.decorator.alice_and_bob.change_gender:71)

========== Example: safari trip gone wrong ==========
Change in Person instance (12345678901 - Alice) attribute date_of_death: to 2025-03-16 from None (by examples.decorator.alice_and_bob.pet_lion:88)

========== Example: log full history of Alice ==========
===== All mutations for Person instance 12345678901 - Alice =====
Created by: examples.decorator.alice_and_bob.main:44
Last mutation by: examples.decorator.alice_and_bob.pet_lion:88
Filled by: None
Number of attribute mutations: 15
Change in Person instance (12345678901 - Alice) attribute social_security_number: to 12345678901 from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:18)
Change in Person instance (12345678901 - Alice) attribute name: to Alice from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:19)
Change in Person instance (12345678901 - Alice) attribute gender: to Female from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:20)
Change in Person instance (12345678901 - Alice) attribute date_of_birth: to 1990-03-07 from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:21)
Change in Person instance (12345678901 - Alice) attribute date_of_death: to None from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:22)
Change in Person instance (12345678901 - Alice) attribute children: to [] from AttributeDoesNotExist (by examples.decorator.alice_and_bob.Person.__init__:23)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles] from [] (by examples.decorator.alice_and_bob.Person.have_child:29)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles, 12312312302 - Davey] from [12312312301 - Charles] (by examples.decorator.alice_and_bob.Person.have_child:29)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312301 - Charles, 12312312302 - Davey, 99889988771 - Fatima] from [12312312301 - Charles, 12312312302 - Davey] (by examples.decorator.alice_and_bob.Person.adopt_child:35)
Change in Person instance (12345678901 - Alice) attribute children: to [12312312302 - Davey, 99889988771 - Fatima] from [12312312301 - Charles, 12312312302 - Davey, 99889988771 - Fatima] (by examples.decorator.alice_and_bob.get_rid_of_child:59)
Change in Person instance (12345678901 - Alice) attribute name: to Bob from Alice (by examples.decorator.alice_and_bob.change_gender:70)
Change in Person instance (12345678901 - Alice) attribute gender: to Male from Female (by examples.decorator.alice_and_bob.change_gender:71)
Change in Person instance (12345678901 - Alice) attribute name: to Alice from Bob (by examples.decorator.alice_and_bob.change_gender:70)
Change in Person instance (12345678901 - Alice) attribute gender: to Female from Male (by examples.decorator.alice_and_bob.change_gender:71)
Change in Person instance (12345678901 - Alice) attribute date_of_death: to 2025-03-16 from None (by examples.decorator.alice_and_bob.pet_lion:88)
Thank you for trying the example with the decorator track_mutations!
```
### Debug mode
Feel free to experience it yourself in debug mode to explore the data in `example_person.MUTATIONS` near the end of the 
example script. There's more data than printed in the log, such as the full trace stack. 

<span id='limitations'></span>
## Limitations
* The mutation will keep the `new_value` as it was at the time of mutation (using `deepcopy`). If it is a mutable type, 
it might be further mutated bypassing the observer functionality because `__setattr__` is not called. 
* The user is prohibited from redefining `__setattr__` and `__new__`  while using `MutationTrackedObject` because it 
will break the observer functionality. If this is blocking for your use, please use the `track_mutations` decorator 
instead.
* The `MutationTrackedObject` functionality will inherit to all child classes of the class actually aimed to be tracked.
Often this is desirable, but it might be undesirable in some cases. If that's the case, please use the 
`track_mutations` decorator instead.

<span id='releasenotes'></span>
## Release notes
No changes since initial release v1.0.1

<span id='hyperlinks'></span>
## Useful links
* <a href='https://github.com/RedmanLabs/mutationtracker'>GitHub</a>
* <a href='https://pypi.org/project/mutationtracker'>PyPi</a>
* <a href='https://www.linkedin.com/in/jaimederrez/'>LinkedIn (Author)</a>

<span id='License'></span>
## License
```
Copyright (c) 2025 Jaime Derrez
All rights reserved.

This code is available under the BSD-license. Read the LICENSE file in the root directory for details.
```