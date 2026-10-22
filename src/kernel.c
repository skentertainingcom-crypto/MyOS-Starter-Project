/* Minimal freestanding kernel: write to VGA text memory and COM1 serial. */

static inline void outb(unsigned short port, unsigned char value)
{
    __asm__ volatile ("outb %0, %1" : : "a"(value), "Nd"(port));
}

static inline unsigned char inb(unsigned short port)
{
    unsigned char value;
    __asm__ volatile ("inb %1, %0" : "=a"(value) : "Nd"(port));
    return value;
}

static void serial_init(void)
{
    /* Configure COM1 for 38400 baud, 8 data bits, no parity, 1 stop bit. */
    outb(0x3F9, 0x00); /* Disable interrupts. */
    outb(0x3FB, 0x80); /* Enable divisor latch. */
    outb(0x3F8, 0x03); /* Divisor low byte. */
    outb(0x3F9, 0x00); /* Divisor high byte. */
    outb(0x3FB, 0x03); /* 8N1; disable divisor latch. */
    outb(0x3FA, 0xC7); /* Enable and clear FIFO. */
    outb(0x3FC, 0x0B); /* Enable IRQs, RTS, and DTR. */
}

static void serial_write_char(char value)
{
    /* Wait for COM1's transmit holding register to become empty. */
    while ((inb(0x3FD) & 0x20) == 0) {
        __asm__ volatile ("pause");
    }
    outb(0x3F8, (unsigned char)value);
}

static void serial_write_string(const char *message)
{
    for (int i = 0; message[i] != '\0'; i++) {
        serial_write_char(message[i]);
    }
}

void kernel_main(void)
{
    volatile unsigned short *screen =
        (volatile unsigned short *)0xB8000;
    const char *message = "Welcome to MyOS!";

    /* Preserve the existing VGA text output exactly. */
    for (int i = 0; message[i] != '\0'; i++) {
        screen[i] = (unsigned short)((0x0F << 8) | (unsigned char)message[i]);
    }

    serial_init();
    serial_write_string(message);
    serial_write_string("\r\n");

    for (;;) {
        __asm__ volatile ("hlt");
    }
}
