SELECT
	id,
	message,
	role
FROM messages
WHERE
	chat_id = :chatId
ORDER BY created_at ASC;