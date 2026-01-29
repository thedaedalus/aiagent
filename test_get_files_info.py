from functions.get_files_info import get_files_info

print("Result for current directory:")
result = get_files_info("calculator", ".")
print("\t" + result.replace("\n", "\n\t"))
print("Result for 'pkg' directory:")
result = get_files_info("calculator", "pkg")
print("\t" + result.replace("\n", "\n\t"))
print("Result for '/bin' directory:")
result = get_files_info("calculator", "/bin")
print("\t" + result.replace("\n", "\n\t"))
print("Result for '../' directory:")
result = get_files_info("calculator", "../")
print("\t" + result.replace("\n", "\n\t"))
