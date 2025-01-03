import type { Meta, StoryObj } from "@storybook/react";
import { generateRandomSchedule } from "@tests/utils/mock-factories";
import { ScheduleBadgeGroup } from ".";

export default {
	title: "UI/ScheduleBadge",
	component: (args) => (
		<div style={{ width: "50px" }}>
			<ScheduleBadgeGroup {...args} />
		</div>
	),
	parameters: {
		layout: "centered",
	},
} satisfies Meta<typeof ScheduleBadgeGroup>;

type Story = StoryObj<typeof ScheduleBadgeGroup>;

export const CollapsedGroup: Story = {
	args: {
		schedules: Array.from({ length: 3 }, () => generateRandomSchedule()),
	},
};