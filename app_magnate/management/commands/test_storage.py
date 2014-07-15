from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    
    help = "Test storage settings for uploading files to Amazon S3 (or elsewhere)."
    
    def handle_noargs(self, **options):
    	# see http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html
    	from django.core.files.storage import default_storage
        from django.conf import settings

        print 'Testing default storage...'
        print 'settings.DEFAULT_FILE_STORAGE=%s' % (getattr(settings, 'DEFAULT_FILE_STORAGE', ''))

        try:
    	   print "Connected to storage: %s" % (default_storage.connection)
        except (AttributeError):
            print 'Storage Location: %s' % (default_storage.base_location)
            print 'Storage Url: %s' % (default_storage.base_url)
        except Exception as e:
            print 'ERROR: connection failure (authentication credentials missing?)'
            print str(e)
            return 1

    	import tempfile
    	# generate a temporary file name
    	# see https://docs.python.org/2.2/lib/module-tempfile.html
    	filename = tempfile.mktemp() # generate random, unique file name
    	data = tempfile.mktemp()     # generate random data (using the same function; why not)


        try:
            # see if we have any access at all
            default_storage.exists(filename) # also see if the filename causes any issues
        except Exception as e: 
            old_filename = filename
            filename = old_filename.replace('/', '_')
            print "WARNING: (%s), so simplifying filename from '%s' to '%s'" % (str(e), old_filename, filename)

        assert not default_storage.exists(filename), "The file '%s' SHOULD NOT exist yet" % (filename)

        print 'OK, creating a file \'%s\'...' % (filename)

        file = default_storage.open(filename, 'w') # open for writing
    	file.write(data)
        file.close()

        assert default_storage.exists(filename), "The file '%s' SHOULD exist now that we've saved it" % (filename)

        print 'OK, reading the file...'

        file = default_storage.open(filename, 'r')
        read_data = file.read()
        file.close()
        assert data == read_data, "Read different data than what we had written (%d bytes and %d bytes), filename '%s'" % (len(read_data), len(data), filename)

        print 'OK, deleting the file...'

        default_storage.delete(filename)

        assert not default_storage.exists(filename), "The file '%s' SHOULD NOT exist now that we've deleted it" % (filename)

        print 'OK, done'