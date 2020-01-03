;;; Number 1

(define (to-usdollar amt cur)
  (cond((eqv? cur 'euro) (/ amt .76))
       ((eqv? cur 'yen ) (/ amt 98.18))
       ((eqv? cur 'won ) (/ amt 1109.85))
       )
  )

(to-usdollar 500 'yen)

;;; Number 2

(define (from-usdollar amt cur)
  (cond((eqv? cur 'euro) (* amt .76))
       ((eqv? cur 'yen ) (* amt 98.18))
       ((eqv? cur 'won ) (* amt 1109.85))
       )
  )

(from-usdollar 1 'yen)

;;; Number 3

(define (convert amt from_cur to_cur)
  (cond((eqv? from_cur 'usd) (cond((eqv? to_cur 'euro) (from-usdollar amt 'euro))
                                  ((eqv? to_cur 'yen ) (from-usdollar amt 'yen))
                                  ((eqv? to_cur 'won ) (from-usdollar amt 'won))
                                  ((eqv? to_cur 'usd ) (amt))
                             ))
       ((eqv? from_cur 'euro) (cond((eqv? to_cur 'usd) (to-usdollar amt 'euro))
                                   ((eqv? to_cur 'yen ) (from-usdollar (to-usdollar amt 'euro) 'yen))
                                   ((eqv? to_cur 'won ) (from-usdollar (to-usdollar amt 'euro) 'won))
                             ))
       ((eqv? from_cur 'yen) (cond((eqv? to_cur 'euro) (from-usdollar (to-usdollar amt 'yen) 'euro))
                                  ((eqv? to_cur 'usd ) (to-usdollar amt 'yen))
                                  ((eqv? to_cur 'won ) (from-usdollar (to-usdollar amt 'yen) 'won))
                             ))
       ((eqv? from_cur 'won) (cond((eqv? to_cur 'euro) (from-usdollar (to-usdollar amt 'won) 'euro))
                                  ((eqv? to_cur 'yen ) (from-usdollar (to-usdollar amt 'won) 'yen))
                                  ((eqv? to_cur 'usd ) (to-usdollar amt 'won))
                             ))))
(convert 1 'yen 'won)

;;; Number 4

(define (squares x n)
  (if (= n 1)
      '()
      (cons (* x x) (squares (+ x 1) (- n 1)))))


(squares 2 12)

;;; Number 5
; reverse
(define (longer? L1 L2)
  (if (null? L1)
      #f
      (if (null? L2)
          #t
          (longer? (cdr L1) (cdr L2))
          )
      )
  )
(longer? '(1 2 3 4) '(1 2 3 4))

;;; Number 6

(define (sum-cash L i)
  (if (> (length L) 0)
      i
      ;(convert (car (car L)) (cdr (car L)) 'usd))
      (sum-cash (cdr L) (+ i 1))
      ))

(sum-cash '((12.20 usd) (1.0 usd) (1.0 usd)) 0)

;;; Number 7

;;; Number 8

(define (notin? L x)
  (if (null? L)
      #f
      (if (eqv? x (car L))
          #t
          (notin? (cdr L) x))))

(define (uniquefy L)
  (if (null? L)
      '()
      (if (notin? (cdr L) (car L) )
          (uniquefy (cdr L))
          (cons (car L) (uniquefy (cdr L)))
          )))
 
(uniquefy '(1 2 3 3 2 5 5 6))

;;; Number 9



