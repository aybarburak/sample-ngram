import sys
import re
import os
import psutil # if this makes an error, you need to install the psutil package on your system
import time

maxmem = 0
def showMemTime(when='Resources'):
  global maxmem
  # memory and time measurement
  process = psutil.Process(os.getpid())
  mem = process.get_memory_info()[0] / float(2 ** 20)
  maxmem = max(maxmem, mem)
  ts = process.get_cpu_times()
  sys.stderr.write("{when:<20}: {mb:4.0f} MB (max {maxmb:4.0f} MB), {user:4.1f} s user, {system:4.1f} s system\n".format(
    when=when, mb=mem, maxmb=maxmem, user=ts.user, system=ts.system))
# NGramCounter class that counts n-tuples of word endings of length m.
class NGramCounter:
  def __init__(self,n,m):
    # initialize storage dictionary (datatype of {} is 'dict')
    self.ngrams = {}
    self.n = n
    self.m = m

  def count(self, *words):
    # if number of given word is not equal to actual desired goal, then give an error to user
    if len(words) != self.n:
        print "Error : number of given words is not equal to required number of ngram"
        return

    # make ngram (datatype of (,) is 'tuple')
    # *words variable keeps given words
    # makes ngram of given word endings of length m
    # run until length of given words, then add to ngram
    ngram = tuple([unicode(words[x], 'utf8')[-self.m:] for x in range(len(words))])

    # increase count for this ngram by one
    if ngram not in self.ngrams:
      # if it was not yet in the dictionary
      self.ngrams[ngram] = 1
    else:
      # if it was already in the dictionary
      self.ngrams[ngram] += 1
    # del ngram after addition to the dictionary
    del ngram

  def display(self):
    showMemTime('begin display')

    # build list of all frequencies and ngrams
    ngram_freq = self.ngrams.items()
    # del ngrams after addition to the frequencies list
    del self.ngrams
    showMemTime('after items')

    # sort that list by frequencies (i.e., second field), descending
    print "sorting ..."
    ngram_freq.sort(key = lambda x:x[1], reverse = True)

    showMemTime('after sorting')

    # iterate over the first five (or less) elements
    print "creating output ..."
    for ngram, occurred in ngram_freq[0:5]:
      print "%d-ending ngram '%s' occured %d times" % \
          (self.m, ("' '".join([str(x.encode('utf-8')) for x in ngram])), occurred)



# this is our main function
def main():
  # make sure the user gave us a file to read
  if len(sys.argv) != 2:
    print "need one argument! (file to read from)"
    sys.exit(-1)
  filename = sys.argv[1]

  showMemTime('begin') # let's observe where we use our memory and time

  # initialize bigram and trigram counter with NGramCounter(n,m) class
  # count n-tuples of word endings of length m
  bc = NGramCounter(2,3)
  tc = NGramCounter(3,2)
  # define first2words variable for keeping first 2 words of each line
  first2words=[]
  # define t variable for 'if the current line is first line of the file,then increase value of t'
  t=0
  # read input file
  print "reading from file "+filename
  f = open(filename,'r')
  # read file one by one line and read back to front
  for line in reversed(list(f)):
      # increase after reading each line
      t+=1

      # split on all newlines and spaces
      inputwords = re.split(r' |\n',line)

      # remove empty strings
      inputwords = filter(lambda x: x != '', inputwords)

      # if length of given line is greater than zero, check following conditions
      if len(inputwords) > 0:
          # value of first2words is empty, next code shouldn't add first2words variable,
          # if the current line is last line of file
          # when current line is not last line fo file,
          # it adds first2words variable to the end of the current line which is given from the previous line
          if first2words != []:
            inputwords+=first2words
          # keep first 2 words of current line for adding to end of the next line
          first2words = inputwords[0:2]

      length = len(inputwords)
      # read inputwords back to front
      for idx in reversed(range(0,length)):

        # count bigram if we can look back one character and if current line is last line of file
        if t==1 and idx <= length - 2:
          bc.count( *(inputwords[idx:idx + 2]))

        # count bigram if we can look back one character and if current line is not last line of file
        if t!=1 and idx <= length - 3:
          bc.count( inputwords[idx], inputwords[idx + 1] )

        # count trigram if we can look back two characters
        if idx <= length - 3:
          tc.count( inputwords[idx], inputwords[idx + 1], inputwords[idx + 2] )

        # if bigram and trigram is counted, then del last word of inputwords
        if idx <= length - 4:
          del inputwords[idx + 3]


  showMemTime('after counting')
  print "bigrams:"
  bc.display()
  print "trigrams:"
  tc.display()

main()
showMemTime('at the end')

