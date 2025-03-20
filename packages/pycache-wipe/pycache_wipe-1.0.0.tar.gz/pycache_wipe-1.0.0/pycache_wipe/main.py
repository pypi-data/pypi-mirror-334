import os
import shutil
import argparse
import sys
import traceback

def delete_pycache(recursive=False):
    try:
        deleted_any = False
        if recursive:
            print("🔍 Recursively searching for __pycache__ directories...")
            for root, dirs, files in os.walk(os.getcwd()):
                if '__pycache__' in dirs:
                    pycache_path = os.path.join(root, '__pycache__')
                    try:
                        shutil.rmtree(pycache_path)
                        print(f"✅ Deleted: {pycache_path}")
                        deleted_any = True
                    except Exception as e:
                        print(f"❌ Failed to delete {pycache_path}: {e}")
                        traceback.print_exc()
        else:
            print("🔍 Searching for __pycache__ in current directory...")
            pycache_path = os.path.join(os.getcwd(), '__pycache__')
            if os.path.exists(pycache_path):
                try:
                    shutil.rmtree(pycache_path)
                    print(f"✅ Deleted: {pycache_path}")
                    deleted_any = True
                except Exception as e:
                    print(f"❌ Failed to delete {pycache_path}: {e}")
                    traceback.print_exc()
            else:
                print("ℹ️ No __pycache__ directory found in current directory.")

        if not deleted_any:
            print("ℹ️ No __pycache__ directories were deleted.")
    except Exception as e:
        print(f"🔥 Unexpected error during deletion: {e}")
        traceback.print_exc()
    finally:
        print("🎉 Finished pycache-wipe operation.")


def main():
    try:
        parser = argparse.ArgumentParser(description='Delete __pycache__ directories.')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-r', '--recursive', action='store_true', help='Delete recursively')
        group.add_argument('-l', '--local', action='store_true', help='Delete only in current directory')
        args = parser.parse_args()

        delete_pycache(recursive=args.recursive)

    except Exception as e:
        print(f"❌ Error parsing arguments or running command: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("👋 Exiting pycache-wipe CLI.")
