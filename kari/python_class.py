
class People:

        def __init__(self, name, age):
		
                self.name = name
                self.age = age

        def introduction(self):

                print("Hi, my name is " + self.name + " and I am " + str(self.age) + " years old.")

        def age_in_n_years(self, n):

                print(self.age + n)


if __name__ == '__main__':
		
        person1 = People("Jess", 27)
        person1.introduction()
        person1.age_in_n_years(10)

        person2 = People("Rory", 48)
        person2.introduction()
        person2.age_in_n_years(10)