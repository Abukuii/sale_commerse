 document.addEventListener("DOMContentLoaded", function () {
            const addToCartButtons = document.querySelectorAll(".add-to-cart");

            addToCartButtons.forEach(function (button) {
                button.addEventListener("click", function (event) {
                    event.preventDefault();
                    const productId = this.getAttribute("data-id");
                    const form = document.getElementById('add-to-cart-form');

                    // Добавляем product_id к форме
                    form.querySelector('input[name="product_id"]').value = productId;

                    // Отправляем POST-запрос на сервер
                    fetch('/add_to_cart/', { // Замените '/add_to_cart/' на URL вашего Django-представления
                        method: 'POST',
                        body: new FormData(form),
                    })
                        .then(response => {
                            if (response.ok) {
                                console.log('Товар успешно добавлен в корзину!');
                                // Здесь можно добавить обновление содержимого корзины на странице
                            } else {
                                console.error('Ошибка при добавлении товара в корзину:', response.status);
                            }
                        })
                        .catch(error => {
                            console.error('Произошла ошибка:', error);
                        });
                });
            });
        });