; ModuleID = "main"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @"printf"(i8* %".1", ...) 

define i32 @"fact"(i32 %".1") 
{
fact_entry:
  %".3" = alloca i32
  store i32 %".1", i32* %".3"
  %".5" = load i32, i32* %".3"
  %".6" = icmp sle i32 %".5", 1
  br i1 %".6", label %"fact_entry.if", label %"fact_entry.endif"
fact_entry.if:
  ret i32 1
fact_entry.endif:
  %".9" = load i32, i32* %".3"
  %".10" = load i32, i32* %".3"
  %".11" = sub i32 %".10", 1
  %".12" = call i32 @"fact"(i32 %".11")
  %".13" = mul i32 %".9", %".12"
  ret i32 %".13"
}

define i32 @"main"() 
{
main_entry:
  %".2" = call i32 @"fact"(i32 5)
  %".3" = alloca i32
  store i32 %".2", i32* %".3"
  %".5" = load i32, i32* %".3"
  %".6" = alloca [21 x i8]
  store [21 x i8] c"fatorial de 5 = %i\0a\00\00", [21 x i8]* %".6"
  %".8" = getelementptr [21 x i8], [21 x i8]* %".6", i32 0, i32 0
  %".9" = call i32 (i8*, ...) @"printf"(i8* %".8", i32 %".5")
  %".10" = load i32, i32* %".3"
  ret i32 %".10"
}
