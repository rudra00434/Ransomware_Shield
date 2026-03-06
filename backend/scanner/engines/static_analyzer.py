import pefile
import math
import hashlib
import time

SUSPICIOUS_APIS = {
    b'CryptEncrypt', b'CryptDecrypt', b'VirtualAlloc', b'VirtualAllocEx',
    b'CreateRemoteThread', b'WriteProcessMemory', b'IsDebuggerPresent',
    b'WNetAddConnection2W', b'WNetOpenEnumW', b'WNetEnumResourceW', # Lateral movement
    b'vssadmin', b'wbem', b'ShadowCopy', # Shadow copy deletion
    b'ShellExecute', b'WinExec', b'Wow64DisableWow64FsRedirection'
}

KNOWN_PACKERS = {
    b'.upx', b'.aspack', b'.enigma', b'.themida', b'.vmp', b'.kdb', 
    b'.mpress', b'.poly', b'pecompact', b'.nsp', b'.ndata'
}

def calculate_entropy(data):
    if not data:
        return 0.0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(bytes([x]))) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def analyze_pe(file_path):
    results = {
        'is_pe': False,
        'entropy': 0.0,
        'imphash': None,
        'suspicious_sections': [],
        'suspicious_imports': [],
        'compiler_timestamp_anomaly': False,
        'error': None
    }
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            results['entropy'] = calculate_entropy(data)
            
        pe = pefile.PE(file_path)
        results['is_pe'] = True
        results['imphash'] = pe.get_imphash()
        
        for section in pe.sections:
            sec_entropy = section.get_entropy()
            name = section.Name.decode('utf-8', errors='ignore').strip('\x00')
            lower_name = section.Name.lower().strip(b'\x00')
            
            # High entropy implies packing/encryption, or name implies known packer
            is_suspicious_packer = any(packer in lower_name for packer in KNOWN_PACKERS)
            if sec_entropy > 7.0 or is_suspicious_packer: 
                results['suspicious_sections'].append({
                    'name': name,
                    'entropy': sec_entropy
                })
                
        # Timestamp anomaly (e.g., compiled before 2000 or in the future)
        timestamp = pe.FILE_HEADER.TimeDateStamp
        current_time = int(time.time())
        if timestamp < 946684800 or timestamp > current_time: # 946684800 is Jan 1, 2000
            results['compiler_timestamp_anomaly'] = True
            
        # Parse Imports
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                for imp in entry.imports:
                    if imp.name:
                        for suspicious_api in SUSPICIOUS_APIS:
                            if suspicious_api.lower() in imp.name.lower():
                                results['suspicious_imports'].append(imp.name.decode('utf-8', errors='ignore'))
                                
    except pefile.PEFormatError:
        results['error'] = 'Not a valid PE file.'
    except Exception as e:
        results['error'] = str(e)
        
    return results
