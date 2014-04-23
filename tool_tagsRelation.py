#!/usr/bin/python
# @author: jingyang
# @email: pagopagi@gmail.com
# create by 2014/4/22

import MySQLdb
import Apriori

# get tags data from db
db = MySQLdb.connect( "localhost", "", "", "" )
cursor = db.cursor()
sql = "SELECT * FROM article_tags LIMIT 0,50000"
tagsdata = {}
try:
	cursor.execute( sql )
	result = cursor.fetchall()
	for row in result:
		tags = []
		id = row[0]
		articleid = row[1]
		tagid = row[2]
		if articleid not in tagsdata:
			tagsdata[articleid] = []
		tagsdata[articleid].append(tagid)
		#print "id is %d, article_id is %s, tag_id is %d" % ( id, articleid, tagid )
except MySQLdb.Error,e:
	print "Error: unable to fecht db! %d: %s" % (e.args[0],e.args[1])

print "data count is ", len( tagsdata )
apriori = Apriori.Apriori( tagsdata )
apriori.main()

db.close()