SELECT
	id,
	source
FROM documents
WHERE
	(user_id = :userId)
	OR (user_id IS NULL AND :userId IS NULL)
ORDER BY created_at DESC;