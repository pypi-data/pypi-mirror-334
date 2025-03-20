import elonadl as elona

def main():
    print("downloading latest version of Elona+ to your %APPDATA% folder")
    elonaplus = elona.download.Download(file_name=elona.ELONA_FILE_NAME, 
                                        link=elona.GH_API_ELONA, 
                                        install_path=elona.INSTALL_PATH)
    elonaplus.create_file()
    elonaplus.get_file()

    print("downloading latest version of CustomGX variant.")
    cgx = elona.download.Download(file_name=elona.CGX_FILE_NAME, 
                                  link=elona.GH_API_CGX, 
                                  install_path=elona.INSTALL_PATH)
    cgx.create_file()
    cgx.get_file()

    print("extracting Elona+")
    e = elona.extract.Extract(elonaplus.get_name(), install_path=elona.INSTALL_PATH)
    e.extract_zip()

    print("extracting CustomGX")
    c = elona.extract.Extract(cgx.get_name(), install_path=elona.INSTALL_PATH)
    c.extract_zip()

    print("Moving files to the latest version")
    mover = elona.move.Move(source_path = cgx.get_install_path(), destination = e.find_latest_version())
    result = mover.execute()
    print(f"Operation {'successful' if result['success'] else 'failed'}")

    print("Renaming Elona+ directory")
    path = e.rename_directory()

    print("Creating Desktop Shortcut")
    version = e.scrape_version()
    d = elona.desktop.Desktop(name=elona.SHORTCUT_NAME, 
                              path=path, 
                              version=version, 
                              exe=elona.EXE, 
                              description=elona.SHORTCUT_NAME)
    d.create_shortcut()

    print("Cleaning up Downloaded Files")
    try:
        cleaner = elona.cleanup.Cleanup(main_game=elona.ELONA_FILE_NAME, 
                                        mod=elona.CGX_FILE_NAME)
        cleaner.execute()
    except Exception as e:
        print(f"Error: {e}")

    print("Creating Start Menu Shortcut")
    menu = elona.start_menu.StartMenu(install_path=path + version 
                                    + "\\" + elona.EXE, 
                                    use_all_users=False,
                                    folder_name=elona.SHORTCUT_NAME, 
                                    current_version=version)
    menu.create_shortcut()

    print('Setup Finished! Enjoy ElonaCustom-GX!')


if __name__ == "__main__":
    main()