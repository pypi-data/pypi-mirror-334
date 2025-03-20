# import packageName.faces as faces
import facedbook.faces as faces
import facedbook.stories as stories
import facedbook.feelings as feelings
import facedbook.encoder as encoder


def main():
    # print(
    #     faces.replace_with_faces(
    #         'All team members must have visibly contributed to the code using their own git & GitHub accounts in order to claim that they contributed to the project.'
    #     ))

    # testing face_story
    print("\nspooky story... \n")
    print(stories.face_story(3))
    print("\nLOOK BEHIND YOU...\n")
    print("BOO!\n")

    # Ask the user how they feel and show a related face emoji
    print("\n Feeling Check! \n")
    print("\n How are you feeling today? (happy, sad, mad, soso): \n")
    print(feelings.ask_user_feeling("happy"))

    # testing face_encoder
    print("\nPrinting happy faces...")
    print(encoder.face_encoder("happy", 8))


if __name__ == "__main__":
    # run the main function
    main()
