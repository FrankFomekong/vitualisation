
def readFeatures():
	p=open('/mnt/nfs_share/features.txt')
	features=p.readlines()
	#print(features)
	p.close()	
	return features[0]
	

st=readFeatures()
out="host,"
dep="3dnow 3dnowext 3dnowprefetch abm acpi adx aes altmovcr8 apic arat avx avx2 avx512-4fmaps avx512-4vnniw avx512bw avx512cd avx512dq avx512er avx512f avx512ifma avx512pf avx512vbmi avx512vl bmi1 bmi2 clflushopt clfsh clwb cmov cmplegacy cmpxchg16 cmpxchg8 cmt cntxid dca de ds dscpl dtes64 erms est extapic f16c ffxsr fma fma4 fpu fsgsbase fxsr hle htt hypervisor ia64 ibs invpcid invtsc lahfsahf lm lwp mca mce misalignsse mmx mmxext monitor movbe mpx msr mtrr nodeid nx ospke osvw osxsave pae page1gb pat pbe pcid pclmulqdq pdcm perfctr_core perfctr_nb pge pku popcnt pse pse36 psn rdrand rdseed rdtscp rtm sha skinit smap smep smx ss sse sse2 sse3 sse4.1 sse4.2 sse4_1 sse4_2 sse4a ssse3 svm svm_decode svm_lbrv svm_npt svm_nrips svm_pausefilt svm_tscrate svm_vmcbclean syscall sysenter tbm tm tm2 topoext tsc tsc-deadline tsc_adjust umip vme vmx wdt x2apic xop xsave xtpr"
lt=st.split(" ")
deps=dep.split(" ")
depslst = {
        # FPU is taken to mean support for the x87 regisers as well as the
        # instructions.  MMX is documented to alias the %MM registers over the
        # x87 %ST registers in hardware.  Correct restoring of error pointers
        # of course makes no sense without there being anything to restore.
        "FPU": ["MMX", "RSTR_FP_ERR_PTRS"],

        # The PSE36 feature indicates that reserved bits in a PSE superpage
        # may be used as extra physical address bits.
       "PSE": ["PSE36"],

        # Entering Long Mode requires that %CR4.PAE is set.  The NX pagetable
        # bit is only representable in the 64bit PTE format offered by PAE.
        "PAE": ["LM", "NX"],

        "TSC": ["TSC_DEADLINE", "RDTSCP", "TSC_ADJUST", "ITSC"],

        # APIC is special, but X2APIC does depend on APIC being available in
        # the first place.
        "APIC": ["X2APIC", "TSC_DEADLINE", "EXTAPIC"],

        # AMD built MMXExtentions and 3DNow as extentions to MMX.
        "MMX": ["MMXEXT", "_3DNOW"],

        # The FXSAVE/FXRSTOR instructions were introduced into hardware before
        # SSE, which is why they behave differently based on %CR4.OSFXSAVE and
        # have their own feature bit.  AMD however introduce the Fast FXSR
        # feature as an optimisation.
        "FXSR": ["FFXSR", "SSE"],

        # SSE is taken to mean support for the %XMM registers as well as the
        # instructions.  Several further instruction sets are built on core
        # %XMM support, without specific inter-dependencies.  Additionally
        # AMD has a special mis-alignment sub-mode.
        "SSE": ["SSE2", "MISALIGNSSE"],

        # SSE2 was re-specified as core instructions for 64bit.  Also ISA
        # extensions dealing with vectors of integers are added here rather
        # than to SSE.
        "SSE2": ["SSE3", "LM", "AESNI", "PCLMULQDQ", "SHA", "GFNI"],

        # Other SSEn each depend on their predecessor versions.  AMD
        # Lisbon/Magny-Cours processors implemented SSE4A without SSSE3.
        "SSE3": ["SSSE3", "SSE4A"],
        "SSSE3": ["SSE4_1"],
        "SSE4_1": ["SSE4_2"],

        # AMD specify no relationship between POPCNT and SSE4.2.  Intel
        # document that SSE4.2 should be checked for before checking for
        # POPCNT.  However, it has its own feature bit, and operates on GPRs
        # rather than %XMM state, so doesn't inherently depend on SSE.
        # Therefore, we do not specify a dependency between SSE4_2 and POPCNT.
        #
        # SSE4_2: [POPCNT]

        # XSAVE is an extra set of instructions for state management, but
        # doesn't constitue new state itself.  Some of the dependent features
        # are instructions built on top of base XSAVE, while others are new
        # instruction groups which are specified to require XSAVE for state
        # management.
        "XSAVE": ["XSAVEOPT", "XSAVEC", "XGETBV1", "XSAVES",
                "AVX", "MPX", "PKU", "LWP"],

        # AVX is taken to mean hardware support for 256bit registers (which in
        # practice depends on the VEX prefix to encode), and the instructions
        # themselves.
        #
        # AVX is not taken to mean support for the VEX prefix itself (nor XOP
        # for the XOP prefix).  VEX/XOP-encoded GPR instructions, such as
        # those from the BMI{1,2}, TBM and LWP sets function fine in the
        # absence of any enabled xstate.
        "AVX": ["FMA", "FMA4", "F16C", "AVX2", "XOP"],

        # This dependency exists solely for the shadow pagetable code.  If the
        # host doesn't have NX support, the shadow pagetable code can't handle
        # SMAP correctly for guests.
        "NX": ["SMAP"],

        # CX16 is only encodable in Long Mode.  LAHF_LM indicates that the
        # SAHF/LAHF instructions are reintroduced in Long Mode.  1GB
        # superpages, PCID and PKU are only available in 4 level paging.
        # NO_LMSL indicates the absense of Long Mode Segment Limits, which
        # have been dropped in hardware.
        "LM": ["CX16", "PCID", "LAHF_LM", "PAGE1GB", "PKU", "NO_LMSL"],

        # AMD K6-2+ and K6-III processors shipped with 3DNow+, beyond the
        # standard 3DNow in the earlier K6 processors.
        "_3DNOW": ["_3DNOWEXT"],

        # This is just the dependency between AVX512 and AVX2 of XSTATE
        # feature flags.  If want to use AVX512, AVX2 must be supported and
        # enabled.  Certain later extensions, acting on 256-bit vectors of
        # integers, better depend on AVX2 than AVX.
        "AVX2": ["AVX512F", "VAES", "VPCLMULQDQ", "AVX_VNNI"],

        # AVX512F is taken to mean hardware support for 512bit registers
        # (which in practice depends on the EVEX prefix to encode) as well
        # as mask registers, and the instructions themselves. All further
        # AVX512 features are built on top of AVX512F
        "AVX512F": ["AVX512DQ", "AVX512_IFMA", "AVX512PF", "AVX512ER", "AVX512CD",
                  "AVX512BW", "AVX512VL", "AVX512_4VNNIW", "AVX512_4FMAPS",
                  "AVX512_VNNI", "AVX512_VPOPCNTDQ", "AVX512_VP2INTERSECT"],

        # AVX512 extensions acting on vectors of bytes/words are made
        # dependents of AVX512BW (as to requiring wider than 16-bit mask
        # registers), despite the SDM not formally making this connection.
        "AVX512BW": ["AVX512_VBMI", "AVX512_VBMI2", "AVX512_BITALG", "AVX512_BF16",
                   "AVX512_FP16"],

        # Extensions with VEX/EVEX encodings keyed to a separate feature
        # flag are made dependents of their respective legacy feature.
        "PCLMULQDQ": ["VPCLMULQDQ"],
        "AESNI": ["VAES"],

        # The features:
        #   * Single Thread Indirect Branch Predictors
        #   * Speculative Store Bypass Disable
        #   * Predictive Store Forward Disable
        #
        # enumerate new bits in MSR_SPEC_CTRL, and technically enumerate
        # MSR_SPEC_CTRL itself.  AMD further enumerates hints to guide OS
        # behaviour.
        #
        # However, no real hardware will exist with e.g. SSBD but not
        # IBRSB/IBRS, and we pass this MSR directly to guests.  Treating them
        # as dependent features simplifies Xen's logic, and prevents the guest
        # from seeing implausible configurations.
        "IBRSB": ["STIBP", "SSBD", "INTEL_PSFD"],
        "IBRS": ["AMD_STIBP", "AMD_SSBD", "PSFD",
               "IBRS_ALWAYS", "IBRS_FAST", "IBRS_SAME_MODE"],
        "AMD_STIBP": ["STIBP_ALWAYS"],

        # In principle the TSXLDTRK insns could also be considered independent.
        "RTM": ["TSXLDTRK"],
    }

#for e in lt:
#    if e in deps:
#        out=out+str(e)+"=1,"
#print(depslst)


def genConfig(flg,ignFlg):
    #deps et out sont des constante que l'on utilise
    ignFlg=ignFlg.split(" ")
    flg=flg.split(" ")
    lst={}
    
    #retirer le flag et ses
    for e in ignFlg:
        lst[e.upper()]=""
    for e in depslst:
        tmp=depslst[e]
        if e.lower() in ignFlg:
            lst[e]=""
        for i in tmp:
            if i.lower() in ignFlg:
                lst[i]=""
                lst[e]=""	
    conf=out
    #gen config
    #print(list(lst.keys()))
                
    for e in flg:
    	if e in deps:
            if e.upper() in list(lst.keys()):
                #print(e.upper())
                #print(list(lst.keys()))
                conf=conf+str(e)+"=0,"
            else:
                conf=conf+str(e)+"=1,"
    #print(list(lst.keys()))        
    return conf,list(lst.keys())


##Test
h=0
#print(len(lt))
match={}
i=1
for e in lt:
    if e in deps:
        #print(h)
        h=h+1
        p,t=genConfig(st,e)
        print(p)
        match['./conf/myvm1'+str(i)+'.cfg']=t
        i=i+1
p=open("mapping.txt",'w')
p.write(str(match).lower())
p.close()
	 
