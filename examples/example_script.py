from pathlib import Path

from shade import Shade
from shade.query_builder import QueryBuilder
from shade.resources.share import DriveRole

"""To run this script, get an API key. Make sure you have a workspace with folders and files at the top level"""


# REMOTE_URL = 'https://api.shade.inc'
REMOTE_URL = 'http://127.0.0.1:9082'

# Add your test key here
API_KEY = 'sk_a11c92d178657a8614316b823f80fa73fe5ffd9adab695b5881f0da4215a3bfd'

# Add the name of your workspace here
WORKSPACE_DOMAIN = 'sebs-playground'


def share_file():
    if shade.share.share_asset(
        drive=drive,
        asset_path=Path(assets[0].get('path')),
        email='emerson@shade.inc',
        role=DriveRole.EDITOR,
        message='Hello you are invited',
    ):
        print('Shared file with user')


def share_folder():
    if shade.share.share_asset(
        drive=drive,
        asset_path=Path(folders[0]),
        email='emerson@shade.inc',
        role=DriveRole.EDITOR,
        message='Hello',
    ):
        print('Shared folder with user')


def get_signed_url():
    signed_url = shade.asset.get_signed_download_url(drive, asset.get('path'))
    print('signed_url', signed_url)


def delete_asset():
    resp = shade.asset.delete_asset(drive=drive, path=Path(assets[0].get('path')))
    if resp:
        print('Deleted asset')


def search_in_folder():
    files = shade.asset.listdir_files(
        drive=drive,
        query=QueryBuilder()
        .set_query('city')
        .set_path('/38d862c3-7699-4ff0-b0fc-9be89c2f85af/shade_tests/places/nyc')
        .limit(50)
        .threshold(0)
        .finish(),
    )

    print(len(files))


def search_similar():
    files = shade.asset.listdir_files(
        drive=drive,
        query=QueryBuilder()
        .set_similar_asset(assets[0])
        .set_path('/38d862c3-7699-4ff0-b0fc-9be89c2f85af/')
        .limit(50)
        .threshold(0)
        .finish(),
    )
    print(files)


def update_asset():
    update = shade.asset.update_asset(
        drive=drive,
        asset=assets[0],
        rating=5,
        category='New Category',
    )

    print(update)


if __name__ == '__main__':
    shade = Shade(remote_url=REMOTE_URL, api_key=API_KEY)

    workspaces = shade.workspace.get_workspaces()

    workspace = shade.workspace.get_workspace_by_domain(workspaces[0].get('domain'))

    drives = shade.drive.get_drives(workspace)

    drive = drives[0]

    assets = shade.asset.listdir_files(
        drive=drive, path=Path('/'), page=0, limit=100
    )  # Note: returns the complete list of assets in directory

    print('assets', assets)

    folders = shade.asset.listdir_folders(
        drive=drive.get('id'),
        path=Path('/'),
        page=0,
        limit=100,  # Returns the path of the folder
    )
    print('folders', folders)

    asset = assets[0]

    drive_metadata = shade.drive.get_custom_metadata(drive)

    person_metadata_field = [
        item
        for item in drive_metadata
        if item.get('description', '').startswith('Check if')
    ][0]

    shade.asset.update_asset_metadata(
        drive,
        asset,
        metadata_attribute_id=person_metadata_field.get('id'),
        metadata_attribute_value=False,
    )

    # Note: uncomment these to run actions
    # share_file()

    # share_folder()

    # delete_asset() Todo only uncomment if there is an asset to delete on the top level of the drive

    # search_in_folder()

    # search_similar()

    # update_asset()

    get_signed_url()
