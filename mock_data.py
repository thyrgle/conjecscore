from sqlmodel import Session
from main import Entry, engine


def main():
    entry1 = Entry(author="Dummy", graph={1:2}, score=3)
    entry2 = Entry(author="Dummy2", graph={1:2}, score=2)
    entry3 = Entry(author="Dummy2", graph={1:2}, score=1)

    with Session(engine) as session:
        session.add(entry1)
        session.add(entry2)
        session.add(entry3)
        
        session.commit()


if __name__ == '__main__':
    main()
