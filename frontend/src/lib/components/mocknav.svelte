    <!-- Header -->
    <header class="sticky top-0 z-30 flex h-16 items-center border-b bg-background px-4 sm:px-6">
        <MainNavbar class="mx-6" />
        <div class="ml-auto flex items-center space-x-4">
          <div class="relative">
            <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input type="search" placeholder="Search transcripts..." class="w-[200px] pl-8 md:w-[300px]" />
          </div>
          <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild let:builder>
              <Button variant="ghost" size="icon" class="rounded-full" builders={[builder]}>
                <User class="h-5 w-5" />
                <span class="sr-only">User menu</span>
              </Button>
            </DropdownMenu.Trigger>
            <DropdownMenu.Content align="end">
              <DropdownMenu.Label>My Account</DropdownMenu.Label>
              <DropdownMenu.Separator />
              <DropdownMenu.Item>Profile</DropdownMenu.Item>
              <DropdownMenu.Item>Settings</DropdownMenu.Item>
              <DropdownMenu.Separator />
              <DropdownMenu.Item>Logout</DropdownMenu.Item>
            </DropdownMenu.Content>
          </DropdownMenu.Root>
        </div>
      </header>





        <!-- Side Navbar -->
  <aside class="fixed inset-y-0 left-0 z-20 hidden w-14 flex-col border-r sm:flex">
    <nav class="flex flex-col items-center gap-4 px-2 py-5">
      <a href="/" class="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-primary-foreground">
        <Package2 class="h-4 w-4" />
        <span class="sr-only">YourApp</span>
      </a>
      <Tooltip.Root>
        <Tooltip.Trigger asChild let:builder>
          <a href="/" class="flex h-9 w-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:text-foreground" use:builder.action {...builder}>
            <House class="h-5 w-5" />
            <span class="sr-only">Dashboard</span>
          </a>
        </Tooltip.Trigger>
        <Tooltip.Content side="right">Dashboard</Tooltip.Content>
      </Tooltip.Root>
      <!-- Add more navigation items as needed -->
    </nav>
    <nav class="mt-auto flex flex-col items-center gap-4 px-2 py-5">
      <Tooltip.Root>
        <Tooltip.Trigger asChild let:builder>
          <a href="/settings" class="flex h-9 w-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:text-foreground" use:builder.action {...builder}>
            <Settings class="h-5 w-5" />
            <span class="sr-only">Settings</span>
          </a>
        </Tooltip.Trigger>
        <Tooltip.Content side="right">Settings</Tooltip.Content>
      </Tooltip.Root>
    </nav>
  </aside>