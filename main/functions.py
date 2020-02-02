def uploadFile(file, ftype):
	if ftype == 'propic':
		file.save('public/propic/' + secure_filename(f.filename))
	elif ftype == 'pic':
		file.save('public/pic/' + secure_filename(f.filename))
	else:
		file.save('public/others/' + secure_filename(f.filename))	
    