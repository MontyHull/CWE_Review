;;; Number 1

(define (to-usdollar amt cur)
  (cond((eqv? cur 'euro) (/ amt .76))
       ((eqv? cur 'yen ) (/ amt 98.18))
       ((eqv? cur 'won ) (/ amt 1109.85))
       )
  )

;(round (to-usdollar 500 'yen))

;;; Number 2

(define (from-usdollar amt cur)
  (cond((eqv? cur 'euro) (* amt .76))
       ((eqv? cur 'yen ) (* amt 98.18))
       ((eqv? cur 'won ) (* amt 1109.85))
       )
  )

;(round (from-usdollar 1 'yen))

;;; Number 3

(define (convert amt from_cur to_cur)
  (cond((eqv? from_cur 'usd) (cond((eqv? to_cur 'euro) (from-usdollar amt 'euro))
                                  ((eqv? to_cur 'yen ) (from-usdollar amt 'yen))
                                  ((eqv? to_cur 'won ) (from-usdollar amt 'won))
                                  ((eqv? to_cur 'usd ) (+ 0 amt))
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

;(round (convert 1 'yen 'won))

;;; Number 4

(define (squares x n)
  (if (= n 1)
      '()
      (cons (* x x) (squares (+ x 1) (- n 1)))))


;(squares 2 12)

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
;(longer? '(1 2 3 4 5) '(1 2 3 4))

;;; Number 6

(define (sum-cash L)
  (if (null? L)
      0
      (+ (convert (car(car L)) (car(cdr(car L))) 'usd) (sum-cash (cdr L)))
      ))


;(round (sum-cash '((12.20 usd) (340 yen) (850 won))))

;;; Number 7
;;;Not complete

  
(define (std-dev L)
  (let ((u (/ (sum L) (length L))))
    (sqrt (/ (sum (square (minusto L u))) (- (length L) 1) ))))

;Sums everything in L
(define (sum L)
  (if (null? L)
      0
      (+ (car L) (sum (cdr L)))))

; subtracts x from every element in L
(define (minusto L x)
  (if (null? L)
      '()
      (cons (- (car L) x) (minusto (cdr L) x))))

;Squares everythin in L
(define (square L)
  (if (null? L)
      '()
      (cons (* (car L) (car L)) (square (cdr L)))
      ))

;(square '(1 2 3))
;(std-dev '(1 2 3))
;(minusto '(1 2 3) 1)
;(round (std-dev '(34 18 25 23 29 11 28 24 27 29)))

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
 
;(uniquefy '(1 2 3 3 2 5 5 6))

;;; Number 9

(define (test-sin x)
  (let ((a (+ 1 (expt (sin x) 2)))) 
    (- (+ (sqrt a ) (/ 1 a)) (expt a 2))))

;(round (test-sin 2))


;;; Number 10
(define (dist x1 y1 x2 y2)
  (let ((L1 (+ (* 12 x1) y1))
        (L2 (+ (* 12 x2) y2)))
    (- L1 L2)))

;(dist 3 7 2 11)

;;; Number 11

(define (f x) (* x x))

(define (fd-at f x)
  (- (f (+ x 1)) (f x)))

;(fd-at f 3)

;;;Number 12
(define (range a b)
  (if (> a b)
      '()
      (cons a (range (+ a 1) b))))

(define (sqrt-prod x)
  (apply * (map sqrt (range 1 x))))

;(sqrt-prod 10)
;(round (sqrt-prod 10))


;;; Number 13
(define (filter pred? L)
  (cond ((null? L) '())
        ((pred? (car L))
         (cons (car L) (filter pred? (cdr L))))
        (else (filter pred? (cdr L)))))

(define (divtres? x)
  (if (= (remainder x 3) 0)
      #t
      #f
      ))

(define (perfsqr? x)
  (if (exact? (sqrt x))
      #t
      #f))

(define (special-nums x)
  (filter divtres? (filter perfsqr? (range 1 x)))
  )
;(special-nums 100)

;;; Number 14
(define P1 '((3 5) (9 2) (11 6) (8 8) (4 6)))

(define (translate L pair)
  (if (null? L)
      '()
      (cons (cons (+ (car(car L)) (car pair)) (cons (+ (car(cdr(car L))) (car(cdr pair))) '())) (translate (cdr L) pair)))) 

;(translate P1 '(1 2))

