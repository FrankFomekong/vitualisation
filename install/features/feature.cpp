#include <bits/stdc++.h>
using namespace std;

int main(){
	int a[4];
	const char* ecx[32]={"fpu","vme","de","pse","tsc","msr","pae","mce","cx8","apic","","sep","mtrr","pge","mca","cmov","pat","pse-36","psn","clfsh","","ds","acpi","mmx","fxsr","sse","sse2","ss","htt","tm","ia64","pbe"};
	const char* edx[32]={"sse3","pclmulqdq","dtes64","monitor","ds-cpl","vmx","smx","est","tm2","ssse3","cnxt-id","sdbg","fma","cx16","xtpr","pdcm","","pcid","dca","sse4.1","sse4.2","x2apic","movbe","popcnt","tsc-deadline","aes","xsave","osxsave","avx","f16c","rdrand","hypervisor"};
	string becx,bedx,oecx,oedx;
	
	__asm__("mov $0x1,%eax\n\t");
	__asm__("cpuid\n\t");

	__asm__("mov %%eax, %0\n\t":"=r" (a[0]));
	__asm__("mov %%ebx, %0\n\t":"=r" (a[1]));
	__asm__("mov %%ecx, %0\n\t":"=r" (a[2]));
	__asm__("mov %%edx, %0\n\t":"=r" (a[3]));
	
	//cout <<a[2] <<endl;
	//cout <<a[3] <<endl;
	//becx=bitset<32>(a[1]).to_string();
	becx=bitset<32>(a[2]).to_string();
	bedx=bitset<32>(a[3]).to_string();
	
	//cout <<becx <<endl;
	//cout <<bedx <<endl;
	oecx="";
	oedx="";
	for(int i=0;i<32;i++){
		if(becx[31-i]=='1' && ecx[i]!=""){
			if(oecx==""){
				oecx=oecx+ecx[i];
			}
			else{
				oecx=oecx+" "+ecx[i]; 
			}
			cout << ecx[i] <<" " ;
		}
	}

	for(int i=0;i<32;i++){
		if(bedx[31-i]=='1' && edx[i]!=""){
                        if(oedx==""){
                                oedx=oedx+edx[i];
                        }
                        else{
                                oedx=oedx+" "+edx[i]; 
                        }
                        cout << edx[i] <<" " ;
                }
	}
	//cout << bitset<32>(a[2]).to_string() <<endl;
	//cout << bitset<32>(a[3]).to_string() <<endl;
	
	return 0;
}
