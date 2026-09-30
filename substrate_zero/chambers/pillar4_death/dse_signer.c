/**
 * dse_signer.c - Demonstrates Compiler Dead-Store Elimination (DSE)
 * 
 * Target: An ephemeral secp256k1 secret scalar is allocated on the stack.
 * The developer dutifully calls memset(scalar, 0, sizeof(scalar)) on exit.
 * Under gcc/clang -O3, the optimizer identifies scalar as a dead store
 * and completely strips the zeroization from the compiled assembly.
 */

#include <stdio.h>
#include <string.h>
#include <stdint.h>

// Marker pattern for easy heap/stack scanning: 0xDEADBEEF...
static const uint8_t TARGET_SECRET[32] = {
    0xde, 0xad, 0xbe, 0xef, 0xca, 0xfe, 0xba, 0xbe,
    0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef,
    0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10,
    0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88
};

// Flawed signing function: memset() is deleted by DSE
__attribute__((noinline))
void sign_transaction_flawed(uint8_t *public_output) {
    uint8_t ephemeral_scalar[32];
    
    // Copy secret scalar into local stack frame
    memcpy(ephemeral_scalar, TARGET_SECRET, 32);
    
    // Simulate ECDSA public commitment: public_output[0..31] = scalar[0..31] ^ 0xAA
    for (int i = 0; i < 32; i++) {
        public_output[i] = ephemeral_scalar[i] ^ 0xAA;
    }
    
    // Developer's intent: Securely zeroize sensitive key scalar before returning
    // [FATAL COMPILER BUG]: Dead-Store Elimination removes this call entirely!
    memset(ephemeral_scalar, 0, sizeof(ephemeral_scalar));
}

int main(void) {
    uint8_t public_sig[32];
    
    printf("[*] Invoking sign_transaction_flawed()...\n");
    sign_transaction_flawed(public_sig);
    
    printf("[*] Function returned. Stack frame deallocated.\n");
    
    // Memory inspect simulation: look at where stack used to be
    volatile uint8_t *stack_probe = public_sig - 64;
    int found_leak = 0;
    
    for (int offset = -128; offset <= 128; offset++) {
        if (memcmp((const void *)(stack_probe + offset), TARGET_SECRET, 16) == 0) {
            found_leak = 1;
            break;
        }
    }
    
    if (found_leak) {
        printf("[!] BREACH: Plaintext secret scalar still resident in stack memory!\n");
        return 42; // Signal leak to caller
    } else {
        printf("[+] Clean: No secret found in stack inspection.\n");
        return 0;
    }
}
