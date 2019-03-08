
import os

def get_not_compare_result(suiteName,logPath):
	for suite in suiteName:
		fd = open(suite,"r")
		resultFile = open(suite[:-4]+".csv","w+")
		resultFile.write("SuiteName,Result,Comment"+"\n")
		lines = fd.readlines()
		for line in lines:
			if ">" in line:
				resultPos = lines.index(line)
				resultName = lines[resultPos].split(">")[-1].replace("bitstreams/","").split(".")[0].strip(" ")
				result = lines[resultPos+1].replace("\n","").strip("-")
				if result == "Failed":
					errlog = get_error_infor(logPath,resultName)
					resultFile.write(resultName+","+result+","+str(errlog)+"\n")
					lines[resultPos] = "Duplicate"
				else:
					resultFile.write(resultName+","+result+"\n")
					lines[resultPos] = "Duplicate"

	fd.close()
	resultFile.close()

def get_compare_result(suiteName,logPath):
	for suite in suiteName:
		fd = open(suite,"r")
		lines = fd.readlines()
		resultFile = open(suite[:-4]+".csv","w+")
		resultFile.write("SuiteName" + "," + "Encode result" + "," + "Compare Result" + "," + "Final Result" + "," + "Comment" + "\n")
		for line in lines:
			if "_TBR" in line:
				resultPos = lines.index(line)
				resultName = lines[resultPos].split(">")[-1].replace("bitstreams/","").split(".")[0].strip(" ")
				result = lines[resultPos+1].replace("\n","").strip("-")
				if result == "Failed":
					errlog = get_error_infor(logPath,resultName)
					resultFile.write(resultName+","+result+","+"Not Compare"+","+result+","+str(errlog)+"\n")
                                	lines[resultPos] = "Duplicate"
				else:
					resultFile.write(resultName+","+result+","+"Not Compare"+","+result+","+"\n")
                                	lines[resultPos] = "Duplicate"
			else:
				continue
		for qp_line in lines:
			if "_Q" in qp_line:
				resultPos = lines.index(qp_line)
				resultName = lines[resultPos].split(">")[-1].replace("bitstreams/","").split(".")[0].strip(" ")
				result = lines[resultPos+1].replace("\n","").strip("-")
				if result == "Enc Error":
					errlog = get_error_infor(logPath,resultName)
					resultFile.write(resultName+","+result+","+"Not Compare"+","+result+","+str(errlog)+"\n")
					lines[resultPos] = "Duplicate"
				elif result == "Passed":
					resultFile.write(resultName+","+result+","+result+","+result+","+"\n")
					lines[resultPos] = "Duplicate"
				elif result == "Failed":
					errlog = get_error_infor(logPath,resultName)
					resultFile.write(resultName+","+"Passed"+","+result+","+result+","+str(errlog)+"\n")
					lines[resultPos] = "Duplicate"
				else:
					resultFile.write(resultName+","+"Passed"+","+""+","+""+"," +"\n")
					lines[resultPos] = "Duplicate"
			else:
				continue
	resultFile.close()
	fd.close()
def get_error_infor(logPath,fileName):
	oripath = os.getcwd()
	os.chdir(logPath)
	errorlog = []
	errFile = open(fileName+".errlog","r")
	errlines = errFile.readlines()
	txtFile = open(fileName+".txt","r")
	txtlines = txtFile.readlines()
	for errline in errlines:
		if "Error" in errline:
			errorlog.append(errline)
		else:
			#print("no error log in errlog file")
			continue
	errFile.close()
	for txtline in txtlines:
		if "Error" in txtline:
			errorlog.append(txtline)
		else:
			continue
	txtFile.close()
	os.chdir(oripath)
	return errorlog


if __name__ == "__main__":
	logPath = r"bitstreams"	#output h265, txt, errlog path
	suiteName = ["me_hme_test.txt","qp_file_test.txt","dlf_test.txt","sao_test.txt" \
                ,"constrained_intra_test.txt","scene_change_test.txt"]
        compareSuite = ["buffered_test.txt","run_to_run_test.txt"]
	get_not_compare_result(suiteName,logPath)
	get_compare_result(compareSuite,logPath)



