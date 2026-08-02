/* libXdamage stub. headless_shell links these four X11 Damage-extension symbols
   but never calls them without an X display, so no-ops satisfy the loader. */
int  XDamageQueryExtension(void *d, int *ev, int *er){ if(ev)*ev=0; if(er)*er=0; return 0; }
unsigned long XDamageCreate(void *d, unsigned long drw, int level){ (void)d;(void)drw;(void)level; return 0; }
void XDamageDestroy(void *d, unsigned long dmg){ (void)d;(void)dmg; }
void XDamageSubtract(void *d, unsigned long dmg, unsigned long r, unsigned long p){ (void)d;(void)dmg;(void)r;(void)p; }
