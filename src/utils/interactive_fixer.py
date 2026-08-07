from src.utils.wiki_manager import create_stub_page


class InteractiveFixer:

    def fix_broken_links(self, broken_links):

        for item in broken_links:

            print("\n--------------------------------")
            print(f"Broken link detected")
            print(f"Page : {item['page']}")
            print(f"Link : {item['broken_link']}")

            print("\n1. Create Stub")
            print("2. Ignore")
            print("3. Rename Link")

            choice = input("\nChoice : ").strip()

            if choice == "1":

                create_stub_page(
                    item["broken_link"],
                    "entity"
                )

                print("Stub Created.")

            elif choice == "2":

                print("Ignored.")

            elif choice == "3":

                new_name = input(
                    "New Link Name : "
                ).strip()

                print(
                    f"Rename '{item['broken_link']}' -> '{new_name}' manually."
                )

            else:

                print("Skipped.")