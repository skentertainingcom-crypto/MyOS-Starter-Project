/* Minimal freestanding kernel: write a message to legacy VGA text memory. */
void kernel_main(void)
{
    volatile unsigned short *screen =
        (volatile unsigned short *)0xB8000;
    const char *message = "Welcome to MyOS!";

    for (int i = 0; message[i] != '\0'; i++) {
        screen[i] = (unsigned short)((0x0F << 8) | (unsigned char)message[i]);
    }

    for (;;) {
        __asm__ volatile ("hlt");
    }
}
