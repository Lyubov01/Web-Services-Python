use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product;

-- 2. Выбрать названия всех автоматизированных складов
select distinct name from store;

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total) from sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select s.store_id from store s where s.store_id in (select store_id from sale s where s.quantity>0);


-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select store_id from store where store_id in (select store_id from store natural left join sale where quantity is NULL or quantity = 0);

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select p.name, avg(s.total/s.quantity) from sale s natural join product p group by product_id;



-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select  p.name from sale natural join product p group by product_id having count(distinct store_id)=1;


-- 8. Получить названия всех складов, с которых продавался только один продукт
select  s.name from store s natural join sale group by store_id having count(distinct product_id)=1;


-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale where total=(select max(total) from sale);

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date from sale group by date order by sum(total) desc,  date asc limit 1;


