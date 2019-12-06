from env_management import (
    create_database, build, initialize, make_settings_table, patch_db,
    populate_test_db)

DB = 'test'
FORCE = True


def make(db, force):
    """Creates the specified database."""
    print("Creating database")
    create_database(force)

    if db == 'production':
        build(verbose=True)
        initialize(verbose=True)
        print("Making settings table")
        make_settings_table()
    elif db == 'test':
        # Test database includes initialization and settings table already
        print("Populating the test database")
        populate_test_db()
        initialize(verbose=True)

    print("Applying patches to database")
    patch_db(verbose=True)
    print("{} environment successfully created".format(db))


make(DB, FORCE)