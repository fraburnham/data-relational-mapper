
(defun tangle-directory (dir)
  (let ((files (directory-files-recursively (expand-file-name dir) "^+*\.org")))
    (dolist (file files)
      (org-babel-tangle-file file))))

(defun tangle-project (project-root)
  (interactive "DProject root: ")
  (message "Tangling project: %s" project-root)
  (tangle-directory project-root))

(add-hook 'org-mode-hook
          (lambda ()
            (add-hook 'after-save-hook 'org-babel-tangle nil 'local)))
