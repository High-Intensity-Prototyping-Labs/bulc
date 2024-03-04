#include <stdio.h>
#include "mantis.h"
#include "mantis/root.h"
#include "mantis/util/util.h"
int main() {
	printf("main() is running...\n");
	mantis();
	root();
	util();

	return 0;
}
