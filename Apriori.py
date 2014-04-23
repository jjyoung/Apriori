#!/usr/bin/python
# @author: jingyang
# @email: pagopagi@gmail.com
# create by 2014/4/22

class Apriori: 
	endTag = False
	tagsdata = {}
	min_support = 0.1 # min support 
	min_conf = 0.6 # min confidence
	level = 1
	
	def __init__( self, data ):
		Apriori.tagsdata = data
		self.dCountMap = []
		self.dkCountMap = []
		self.confItemset = []

	def dump( self, content ):
		print content

	def main( self ):
		cItemset = self.findFirstCandidate( Apriori.tagsdata);
		print "--------- leve 0 ----------------"
		print "<<<<<<<<<<<<<<<<<<<<<<<<<<<< cItemset ", len( cItemset )
		#self.dump( cItemset );
		#self.dump( self.linelist );
		lItemset = self.getSupportedItemset( cItemset );
		while Apriori.endTag != True:
			print
			print "--------- leve %d ----------------" % Apriori.level
			print ">>>>>>>>>>>>>>>>>>>>>>>>>>>> lkItemset ", len( lItemset )
			self.dump( lItemset )
			ckItemset = self.getNextCandidate( lItemset );
			print "<<<<<<<<<<<<<<<<<<<<<<<<<<<< ckItemset ", len( ckItemset )
			self.dump( ckItemset )
			lkItemset = self.getSupportedItemset( ckItemset );
			print ">>>>>>>>>>>>>>>>>>>>>>>>>>>> lkItemset ", len( lkItemset )
			self.dump( lkItemset )
			self.getConfidencedItemset( lkItemset, lItemset, self.dkCountMap, self.dCountMap )
			print ">>>>>>>>>>>>>>>>>>>>>>>>>>>> confItemset ", len( self.confItemset )
			print self.confItemset
			if len( self.confItemset ) > 0:
				print self.confItemset
			cItemset = ckItemset
			lItemset = lkItemset
			del self.dCountMap
			self.dCountMap = self.dkCountMap
			Apriori.level += 1
		print "<<<<<<<<<<<<<<<<<<<<"
		print self.confItemset

	def findFirstCandidate( self, data ):
		tablelist = []
		lineList = []
		for i in data:
			for j in data[i]:
				if j not in lineList:
					lineList.append(j)
		self.linelist = lineList

		for j in lineList:
			list = []
			list.append(j)
			tablelist.append( list )
			
		return tablelist

	def getSupportedItemset( self, itemset ):
		supportItemset = []
		end = True
		index = 0
		for i in range( len( itemset ) ):
			count = self.countFrequent( itemset[i] )
			support = Apriori.min_support * ( ( len( Apriori.tagsdata ) - 1 ) * 1.0 )
			#print "id %d, count %d, support %d " % ( itemset[i][0], count, support )
			if count >= support:
				index += 1
				print "id: %d --------------- index: %d, count : %d, support is %d " % ( itemset[i][0], index, count, support )
				if len( itemset[0] ) == 1 :
					self.dCountMap.insert( index, count )
				else:
					self.dkCountMap.insert( index, count )
				supportItemset.append(itemset[i])
				end = False

		#print self.dCountMap
		Apriori.endTag = end
		return supportItemset

	def countFrequent( self, list ):
		count = 0
		for i in Apriori.tagsdata:
			notHaveThisList = False
			for j in range( len( list ) ):
				thisRecordHave = False
				for h in Apriori.tagsdata[i]:
					if list[j] == h:
						thisRecordHave = True
				if thisRecordHave == False:
					notHaveThisList = True
					break
			if notHaveThisList == False:
				count += 1
		return count

	def getNextCandidate( self, lItemset ):
		nextItemset = []
		for i in range( len(lItemset) ):
			temp = []
			for t in range( len(lItemset[i]) ):
				temp.append( lItemset[i][t] )
			#print temp
			#print "-------------"
			for h in range( i+1, len(lItemset) ):
				for j in range( len( lItemset[h] ) ):
					temp.append( lItemset[h][j] )
			#		print temp
			#		print "+++++++++++"
					have = self.isSubsetInC( temp, lItemset )
			#		print "have item is ", have
					if have == True :
						copyValueList = []
						for n in range( len( temp ) ):
							copyValueList.append( temp[n] )
							if self.isHave( copyValueList, nextItemset ):
								nextItemset.append( copyValueList )
					del temp[len(temp)-1]

		return nextItemset	

	def isSubsetInC( self, tempList, cItemset ):
		haveTag = False
		for i in range( len( tempList ) ):
			testList = []
			for j in range( len( tempList ) ):
				if i != j:
					testList.append( tempList[j] )
			#print testList
			#print "=============test list "
			for h in range( len( cItemset ) ):
				if testList == cItemset[h]:
					haveTag = True
					break;
			if haveTag == False:
				return False
		return haveTag

	def isHave( self, copyValueList, nextItemset ):
		for i in range( len( nextItemset ) ):
			if copyValueList == nextItemset[i] :
				return False
		return True

	def getConfidencedItemset( self, lkItemset, lItemset, dkCountMap, dCountMap ):
		for i in range( len( lkItemset ) ):
			self.getConfItem( lkItemset[i], lItemset, dkCountMap[i], dCountMap );

	def getConfItem( self, list, lItemset, count, countMap ):
		#print "count map ", countMap
		for i in range( len( list ) ):
			testList = []
			for j in range( len( list ) ):
				if i != j :
					testList.append( list[j] )
			index = self.findConf( testList, lItemset )
			conf = 0.0
			conf = count*1.0 / countMap[index]
			#print "test list is " , testList
			print "test list conf is ", conf
			#print "index: %d, count: %d-------%d" % ( index, count, countMap[index])
			if conf > Apriori.min_conf :
				testList.append( list[i] )
				relativeSupport = 0.0
				relativeSupport = count*1.0 / ( len( Apriori.tagsdata ) - 1 )
				print "relative support " , relativeSupport
				testList.append( relativeSupport )
				testList.append( conf )
				self.confItemset.append( testList )

	def findConf( self, testList, lItemset ):
		for i in range( len( lItemset ) ):
			notHaveTag = False
			for j in range( len( testList ) ):
				if self.haveThisItem( testList[j], lItemset[i] ) == False:
					notHaveTag = True
					break
			if notHaveTag == False:
				return i
		return -1
				
	def haveThisItem( self, item, list ):
		for i in range( len( list ) ):
			if item == list[i]:
				return True;
		return False

