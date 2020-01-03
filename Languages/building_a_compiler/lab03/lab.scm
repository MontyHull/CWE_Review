;;; Question 1 - done
      
(define (min-sin x . vals)
    (sin-check (apply min (map sin (cons x vals))) (cons x vals)))
    

(define (sin-check x L)
  (if (eqv? x (sin (car L)))
      (car L)
      (sin-check x (cdr L))
      )
  )

;(min-sin 1.1 2.3 4.5 6.7)

;;;Question 2 - done
(define (extract x L)
  (if (eq? 0 x)
      '()
      (if (null? L)
          '()
          (cons (car L) (extract (- x 1) (cdr L))))))

(define (remove-x x L)
  (if (eq? 0 x)
      L
      (if (null? L)
          L
          (remove-x (- x 1) (cdr L)))))



(define (grouphelp x L)
  (if (null? L)
  '()
  (cons (extract x L) (grouphelp x (remove-x x L)))))

(define (group x . L)
  (grouphelp x L))

;(group 2 'a 1 'b 2 'c 3 'd)

;;;Question 3 - done
(define (pow x y z)
  (if (eq? 1 x)
      z
      (pow (- x 1) y (* y z))))

(define (power n)
  (lambda (x)
    (pow n x x)))

      
(define cube (power 3))

;;;Question 4 - done

; determines if x is a car or a cdr
(define (car-or-cdr x vals L)
  (if (null? vals)
      (if (eq? x 'a)
          (car L)
          (cdr L)
          )
      (if (eq? (car vals) 'a)
          (car-or-cdr x (cdr vals) (car L))
          (car-or-cdr x (cdr vals) (cdr L)))))

;Make a car/cdr function
(define (make-cXr x . val)
  (lambda (L)
    (car-or-cdr x (reverse val) L)))

(define caaaaaadr (make-cXr 'a 'a 'a 'a 'a 'a 'd))

;(caaaaaadr '((1 2) ((((((3))))))))

;;;Question 5 - done
(define (make-stack)
  (let ((stackss '()))
    (lambda (message . data)
      (cond ((eqv? message 'size)
             (length stackss))
            
            ((eqv? message 'push)
             (set! stackss (append data stackss)))
            
            ((eqv? message 'pop)
             (begin
               (display (car stackss))
               (newline)
               (set! stackss (cdr stackss))))
            )
      )))

#|
(define s1 (make-stack))
(s1 'size)
(s1 'push 3 'a 2.1)
(s1 'pop)
(s1 'push 'x)
(s1 'pop)
(s1 'pop)
(s1 'size)
|#

;;;Question 6/7 done

;Sorts a list from min to max with only distinct numbers 
(define (sort-list L)
  (if (null? L)
      '()
      (cons (apply min L) (sort-list (remove (apply min L) L)))
      )
  )

;Removes x from list L
(define (remove x L)
  (if (null? L)
      '()
      (if (eqv? x (car L))
          (remove x (cdr L))
          (cons (car L) (remove x (cdr L))))))

(define (in? x L)
  (if (null? L)
      #f
      (if (eqv? x (car L))
          #t
          (in? x (cdr L))
          )
      )
  )

(define (make-set)
  (let ((set '()))
    (lambda (message . data)
      (cond ((eqv? message 'get)
             (sort-list set))
            ((eqv? message 'set!)
             (set! set (car data)))
            ((eqv? message 'size)
             (length (sort-list set)))
            ((eqv? message 'insert)
             (set! set (append (sort-list data) set)))
            ((eqv? message 'contains?)
             (in? (car data) set))
            ))))
#|
(define set1 (make-set))
(set1 'get)
(set1 'set! (list 15))
(set1 'get)
(set1 'size)
(set1 'insert 10)
(set1 'get)
(set1 'size)
(set1 'contains? 9)
|#


;;;Question 10

;;Question 2 tail-recursive
#|
(define (grouphelp x L)
  (if (null? L)
  '()
  (cons (extract x L) (grouphelp x (remove x L)))))
|#
(define (grouphelp-tr x L accum)
  (if (null? L)
  (reverse accum)
  (grouphelp-tr x (remove-x x L) (cons (extract x L) accum)))) 
  ;(cons (extract x L) (grouphelp x (remove x (cdr L))))))

(define (group-tr x . L)
  (grouphelp-tr x L '()))

  
;(group-tr 2 'a 1 'b 2 'c 3 'd)
 

  
