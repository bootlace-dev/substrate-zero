/**
 * dse_signer_patched.c - Demonstrates Secure Zeroization Immune to DSE
 * 
 * Uses memory barriers (asm volatile("" : : "r"(buf) : "memory")) or
 * explicit_bzero to guarantee the compiler cannot optimize away memory clearing.
 */

#include <stdio.h>
#include <string.h>
#include <stdint.h>

static const uint8_t TARGET_SECRET[32] = {
    0xde, 0xad, 0xbe, 0xef, 0xca, 0xfe, 0xba, 0xbe,
    0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef,
    0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10,
    0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88
};

// Hardened zeroization helper using volatile assembly memory barrier
static void secure_memzero(void *ptr, size_t len) {
    memset(ptr, 0, len);
    // Assembly memory barrier forces compiler to treat buffer as read/written
    __asm__ __volatile__("" : : "r"(ptr) : "memory");
}

__attribute__((noinline))
void sign_transaction_secure(uint8_t *public_output) {
    uint8_t ephemeral_scalar[32];
    
    memcpy(ephemeral_scalar, TARGET_SECRET, 32);
    
    for (int i = 0; i < 32; i++) {
        public_output[i] = ephemeral_scalar[i] ^ 0xAA;
    }
    
    // HARDENED: Secure zeroization immune to Dead-Store Elimination
    secure_memzero(ephemeral_scalar, sizeof(ephemeral_scalar));
}

int main(void) {
    uint8_t public_sig[32];
    
    printf("[*] Invoking sign_transaction_secure()...\n");
    sign_transaction_secure(public_sig);
    
    printf("[*] Function returned. Stack frame sanitized.\n");
    
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
        return 42;
    } else {
        printf("[+] Clean: Ephemeral key successfully sanitized from memory.\n");
        return 0;
    }
}
