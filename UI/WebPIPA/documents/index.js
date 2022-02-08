function getTableColumns () {
  var fs = require('fs')
  var data = fs.readFileSync('./Kleborate.txt',
    { encoding: 'utf8', flag: 'r' })
  return (data.split('\n')[0]).split('\t')
}