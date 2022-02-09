use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product;

-- 2. Выбрать названия всех автоматизированных складов
select name from store;

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total) from sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select distinct(store_id) from sale
where quantity > 1;

-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select store.store_id from sale
right join store on sale.store_id = store.store_id
where quantity is null;

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select product.name, avg(total/quantity) from sale
right join product on sale.product_id = product.product_id
where quantity is not null
group by sale.product_id;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select product.name from sale
inner join product on sale.product_id = product.product_id
group by sale.product_id
having count(distinct store_id) = 1;

-- 8. Получить названия всех складов, с которых продавался только один продукт
select store.name from sale
inner join store on sale.store_id = store.store_id
group by sale.store_id
having count(distinct product_id) = 1;

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale
where total = (select max(total) from sale);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select xxx.date from (select date, sum(total) as sum from sale group by date)xxx
where xxx.sum = (select max(xxx.sum) from (select date, sum(total) as sum from sale group by date)xxx);
