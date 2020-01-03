;;; SI 413 Lab 1
;;; MIDN Hall

;;; Exercise 1 ;;;
(define ex1
  (+ (* (- 34.453 47.728) 4.7) 3.7)
  )

;;; Exercise 2 ;;;
;;; something weird about division?
(define ex2
  (max
   (sqrt 5)
   (+ (sin 1) (sin 2) (sin 3))
   (/ 31 13)
   )
  )
;;; Exercise 3 ;;;
(define ex3
  (- (+ (- (* 2 2.451 2.451 2.451) (* 2.451 2.451)) (* 3 2.451)) 5)
  )

;;; Exercise 4 ;;;
(define root2 (sqrt 2))

;;; Exercise 5 ;;;
(define (to-celsius x)
  (*(/ 5 9) (- x 32))
  )

(define (to-fahrenheit x)
  (+ (*(/ 9 5) x) 32)
  )

;;; Exercise 6 ;;;
(define (test-trig x)
  (+ (*(sin x) (sin x)) (*(cos x) x))
  )

;;; Exercise 7 ;;;
( define (signed-inc x)
   (if (< x 0)
       (+ -1 x)
       (+ 1 x))
   )

;;; Exercise 8 ;;;
( define (signed-inc-better x)
   (if (< x 0)
       (+ -1 x)
       (if (> x 0)
           (+ 1 x)
           0))
   )

;;; Exercise 9 ;;;
(define (middle x y z)
  (if(> x y)
     (if(< x z)
        x
        (if (> y z)
            y
            z
            )
        )
     (if(> x z)
        x
        (if(> y z)
           z
           y
           )
        )
     )
  )

;;; Exercise 10 ;;;
;;; not finished ;;;

;;; Exercise 11 ;;;
;;; Java would not have given me this result because it is to large to fit in a
;;; normal type. it is 599 bits so it will overflow
(define (factorial x)
  (if (= x 1)
      x
      (* x (factorial (- x 1)))
      )
  )


;;; Exercise 12

;(define (compound-month B r)
; (* B (/ r 100)))
  

;(define (accrue-months B r m)
;  (if (= m 0)
;      B
;      (+ (compound-month B r) (accrue-months B r (- m 1))))) 

;(compound-month 100 10)
;(accrue-months 100 10 3)


;;; Exercise 13

(define (fib x)
  (cond((= x 1) 1)
       ((= x 2) 1)
       (else (+ (fib(- x 1)) (fib(- x 2))))))

;;;Exercise 14

(define (split-inches x)
  (cons (quotient x 12) (remainder x 12) ) )


;;; Exercise 15

(define (shorter? x y)
  (< (+ (* (car x) 12) (cdr x)) (+ (* (car y) 12) (cdr y))))

