from simple_mongo.database import MongoDB
def main():
    result = MongoDB.create('users', {'name': 'John Doe', 'email': 'johndoe@gmail.com'})

    if result:
        print('Document inserted successfully')
    else:
        print('Document insertion failed')

    MongoDB.all('users')


if __name__ == '__main__':
    main()
# What will be the output of the above code?