document.addEventListener('DOMContentLoaded', function () {
    const dropdownLinks = document.querySelectorAll('.nav-item.dropdown > a');

    dropdownLinks.forEach(link => {
        const dropdownMenu = link.nextElementSibling;

        link.addEventListener('click', function (e) {
            const isOpen = dropdownMenu.style.display === 'block';

            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                if (menu !== dropdownMenu) menu.style.display = 'none';
            });

            if (isOpen) {
                e.preventDefault();
                dropdownMenu.style.display = 'none';
            } else {
                dropdownMenu.style.display = 'block';
            }
        });

        link.addEventListener('keydown', function (e) {
            if (e.key === ' ') {
                e.preventDefault();
                const isOpen = dropdownMenu.style.display === 'block';

                document.querySelectorAll('.dropdown-menu').forEach(menu => {
                    if (menu !== dropdownMenu) menu.style.display = 'none';
                });

                dropdownMenu.style.display = isOpen ? 'none' : 'block';
            }
        });
    });

    document.addEventListener('click', function (e) {
        if (!e.target.closest('.nav-item.dropdown')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });
});