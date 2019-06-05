#make 1 vcard file for all contacts and 1 for each person
import csv

with open('list1.csv', 'r') as csv_file:
    reader = csv.reader(csv_file)
    csv_file.readline()   #skips first line
    allvcf = open('all contacts.vcf', 'w')
    i = 0

    for row in reader:
        vcf = open(row[0] + ' ' + row[1] + '.vcf', 'w')
        vcf.write( 'BEGIN:VCARD' + "\n")
        vcf.write( 'VERSION:3.0' + "\n")
        vcf.write( 'N:' + row[0] + ';' + row[1] + "\n")
        vcf.write( 'FN:' + row[1] + ' ' + row[0] + "\n")
        vcf.write( 'ORG:' + row[2] + "\n")
        vcf.write( 'TEL;CELL:' + row[3] + "\n")
        vcf.write( 'EMAIL:' + row[4] + "\n")
        vcf.write( 'END:VCARD' + "\n")
        vcf.write( "\n")
        vcf.close()

        #write in the "ALL.vcf" file
        allvcf.write( 'BEGIN:VCARD' + "\n")
        allvcf.write( 'VERSION:3.0' + "\n")
        allvcf.write( 'N:' + row[0] + ';' + row[1] + "\n")
        allvcf.write( 'FN:' + row[1] + ' ' + row[0] + "\n")
        allvcf.write( 'ORG:' + row[2] + "\n")
        allvcf.write( 'TEL;CELL:' + row[3] + "\n")
        allvcf.write( 'EMAIL:' + row[4] + "\n")
        allvcf.write( 'END:VCARD' + "\n")
        allvcf.write( "\n")

        i += 1

    allvcf.close()
    print(str(i+1) + ' vcf cards created')
