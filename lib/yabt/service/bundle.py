#!/usr/bin/env python3



# pylint: disable=line-too-long



import yabt
import sys
import os
import zipfile
import subprocess



def extract(bundle_name):
	"""Expand the service bundle into a directory.
	"""

	bundle_name_base = os.path.basename(bundle_name)

	if not bundle_name == bundle_name_base:
		os.rename(bundle_name, bundle_name_base)

		print("Moved", bundle_name_base, "to the current working directory")

		bundle_name = bundle_name_base

	bundle_dir = bundle_name[:-4]

	print("Extracting service bundle to", bundle_dir)

	os.mkdir(bundle_dir)

	try:
		zip_ref = zipfile.ZipFile(bundle_name, "r")
		zip_ref.extractall(bundle_dir)
		zip_ref.close()

	except zipfile.BadZipFile:
		print("Failed to extract bundle, corrupt zip?  Attempting to extract with 7zip", file=sys.stderr)

		zip7_command = shutil.which("7z")

		if zip7_command is None:
			print("7zip command (7z) not found.  Please install 7zip.", file=sys.stderr)

			sys.exit(1)

		zip7_process = subprocess.Popen([zip7_command, "x", "-o" + bundle_dir, "-y", bundle_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		zip7_process.wait()

		# Note that we're not checking if 7zip was successful because it will exit non-zero even if it was able to partially extract the zip.

	return bundle_dir

